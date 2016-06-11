#!/usr/bin/python

#import sys
#import json
#import subprocess
import mechanize
import urlparse
import urllib,urllib2
from bs4 import BeautifulSoup
import multiprocessing

class Search:
	"""Search class for new google search"""

	def __init__(self, keyword):
		self.keyword = keyword
		self.crawl_topic = 'escort'
		self.preprocessQuery()

		self.chrome = mechanize.Browser(factory=mechanize.RobustFactory())
		self.chrome.set_handle_robots(False)
		self.chrome.addheaders = [('User-agent','Mozilla/5.0')]
		self.chrome.open("http://www.google.com")
		self.chrome.select_form(name='f')

	def googleSearch(self) :
		"""Do the query"""
		
		self.chrome.form['q'] = self.keyword

		response = self.chrome.submit()

		soup = BeautifulSoup(response.read())

		self.search_results = []

		for a in soup.select(".r a") :
			self.search_results.append(urlparse.parse_qs(urlparse.urlparse(a['href']).query)['q'][0])
		
		#response = self.chrome.follow_link(text='Next')

		#soup = BeautifulSoup(response.read())

		#for a in soup.select(".r a") :
		#	self.search_results.append(urlparse.parse_qs(urlparse.urlparse(a['href']).query)['q'][0])		

	def get_crawled_urls(self) :

		self.all_urls = []

		for url in self.search_results :
			
			url_entry = {}

			try:
				req = urllib2.Request(url, headers={'User-agent':'Mozilla/5.0'})
				response = urllib2.urlopen(req)
				
			except Exception, e:
				continue

			url_entry['url'] = url
			url_entry['html'] = response.read() #req.text

			self.all_urls.append(url_entry)
		
	def preprocessQuery(self):

		self.keyword = self.keyword.lower()

		keywords_all = self.keyword.split();

		if self.crawl_topic not in keywords_all:
			keywords_all.append(self.crawl_topic)

		self.keyword = ('+').join(keywords_all)