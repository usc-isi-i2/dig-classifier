#!/usr/bin/python

import sys
import json
import subprocess
import time
import urllib, urllib2
import requests
from tfidf_vectorize import compute_ngrams

class Crawler:
	"""New crawler instance"""
	def __init__(self, args):
		self.query = args
		self.search_terms = {}
		self.job_id = None
		self.url = "http://localhost/api/fetch-searchterm/"

		self.search_terms[args] = "query_"+self.query		
	
	def add_query_keywords(self) :
		keywords = compute_ngrams(self.query.split(), (2,2))

		requests.put('http://localhost/api/keyword/', data=json.dumps(keywords), headers={'content-type':'application/json'})

	def create_new_workspace(self) :
		self.workspace_name = '_'.join(self.query.split())

		# Check if workspace with same name already exists
		response = requests.get('http://localhost/api/get-workspace-id/'+self.workspace_name+'/')

		# If exists delete
		wsp_id = response.json()['id']
		if wsp_id != None :
			requests.put('http://localhost/api/workspace/selected-by-name/default/')
			requests.delete('http://localhost/api/workspace/'+wsp_id+'/')

		# Add new workspace
		requests.put('http://localhost/api/workspace/'+self.workspace_name+'/')
		requests.put('http://localhost/api/workspace/selected-by-name/'+self.workspace_name+'/')

	def schedule_crawler(self) :
		""" Start a new crawl with search_terms"""
		self.create_new_workspace()
		#self.add_query_keywords()

		req = urllib2.Request(self.url, json.dumps(self.search_terms), {"Content-type" : "application/json"})

		try:
			response = urllib2.urlopen(req)
		except IOError, e:
		    print "It looks like something went wrong in scheduling the crawl. Exiting..."
		    sys.exit(1)

		out = json.loads(response.read())
		
		self.job_id = out.keys()[0]

		print "Crawling in progress ...";
		
		
	def wait_for_crawl(self) :
		""" Wait till crawler completes"""
		
		data = {'job_id' : self.job_id}
		url_values = urllib.urlencode(data)
		req_url = "http://localhost/search-job-state/?" + url_values

		while(1) :
			try:
				response = urllib2.urlopen(req_url)
			except IOError, e:
				print "It looks like something went wrong"
				sys.exit(1)
		
			state = response.read()

			if(state == 'Done') :
				print "Crawl complete !"
				return

	def get_crawled_hosts(self) :

		self.hosts_crawled = []
		i = 0

		while 1 :
			url = "http://localhost/hosts/" + str(i)
			req = urllib2.Request(url, headers = {"Accept" : "application/json"})

			try:
				response = urllib2.urlopen(req)
			except IOError, e:
				print "It looks like something went wrong"
				return
		
			json_output = json.loads(response.read())

			if len(json_output) == 0 :
				return

			for host_index in range(len(json_output)) :
				self.hosts_crawled.append(json_output[host_index]['host'])

			i += 1

	def get_crawled_urls(self) :

		target_keys = ['url', 'html']
	
		self.all_urls = []

		for host in self.hosts_crawled :
			
			url = "http://localhost/urls/"+host
			req = urllib2.Request(url, headers={"Accept":"application/json"})

			try:
				response = urllib2.urlopen(req)
				json_output = json.loads(response.read())
			except IOError, e:
				print "It looks like something went wrong"
				break
			
			for url_entry in json_output :
				
				# Ignore urls with form parameters
				if '?' in url_entry['url'] :
					continue
				
				for key in url_entry.keys() :
					if key not in target_keys :
						del url_entry[key]

				self.all_urls.append(url_entry)

		