#!/usr/bin/python

import re
import sys
import json
import subprocess
import urlparse
import urllib, urllib2, base64

class Dig_Search:
    """Dig Search request object"""
    def __init__(self, query_string):
        self.query_string = query_string
        self.url = "https://esc.memexproxy.com/dig-latest/WebPage/_search"
        self.username = "darpamemex"
        self.password = "darpamemex"
        self.size = 1000	
        self.dig_query = {'query': {'query_string': {'query': self.query_string,'default_operator': 'AND'}}, 'size':self.size, '_source':['url','hasBodyPart']}
        self.dig_output = None
        
    def search_request(self) :
        """Perform search query in dig"""
        
        data = json.dumps(self.dig_query)
        req = urllib2.Request(self.url, data, {"Content-type" : "application/json"})
        
        base64string = base64.encodestring('%s:%s' % (self.username, self.password)).strip()
        authheader =  "Basic %s" % base64string
        req.add_header("Authorization", authheader)
        try:
            response = urllib2.urlopen(req)
        except IOError, e:
            print "It looks like the username or password is wrong."
            sys.exit(1)
            
        self.dig_output = response.read()
        
    def dig_extraction(self) :	
        all_hits = json.loads(self.dig_output)['hits']['hits']
        
        assert len(all_hits) > 0, "No dig results found for this query"
        
        self.urls_dig = []
        
        for hit in all_hits :
            url = hit['_source']['url']
            html = self.extract_html(hit['_source'])
            
            if html == None :
                continue
            
            url_temp = '/'.join(urlparse.urlparse(url)[2:])
            
            for d in ['$','-', '_', '.', '+', '!', '*', '(', ')', '/',':'] :
                url_temp = url_temp.replace(d, ' ')
                
            url_entry = {}
            url_entry['url'] = url.encode(encoding='ascii',errors='ignore')
            url_entry['html'] = html + " " + url_temp
                
            self.urls_dig.append(url_entry)
        
        assert len(self.urls_dig) > 0, "No dig results found for this query"

    def extract_html(self, hit) :
        
        try:
            html = hit['hasBodyPart']['text']
            if len(html) < 50 :
                html = None
        except Exception:
            return None
        finally:
            return html
            
    def filter_dig_result(self, data) :
        self.urls_dig = data[0:100]
		