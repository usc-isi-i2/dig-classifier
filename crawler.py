#!/usr/bin/python

import mechanize
import urlparse
import urllib,urllib2
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool
import re

class Search:
    """Search class for new google search"""

    def __init__(self, keyword):
        self.keyword = keyword
        self.crawl_topic = 'escort'
        self.preprocessQuery()
        
        try :
            self.chrome = mechanize.Browser(factory=mechanize.RobustFactory())
            self.chrome.set_handle_robots(False)
            self.chrome.addheaders = [('User-agent','Mozilla/5.0')]
            self.chrome.open("http://www.google.com")
            self.chrome.select_form(name='f')
        except Exception as e:
            print "ERROR!!!"            
            print e

    def googleSearch(self) :
        """Do the query"""
        self.chrome.form['q'] = self.keyword
        
        self.search_results = []
        
        try :        
            response = self.chrome.submit()
        except Exception as e :
            print e
            
        for i in range(3) :
            soup = BeautifulSoup(response.read())
            
            try :
                for a in soup.select(".r a") :
                    self.search_results.append(urlparse.parse_qs(urlparse.urlparse(a['href']).query)['q'][0])
            except ValueError as ve :
                print ve
            
            response = self.chrome.follow_link(text='Next')

    def get_crawled_urls(self) :
        pool = ThreadPool(12)
        
        self.all_urls = pool.map(self.get_url_content, self.search_results)
        
        pool.close()
        pool.join()
        
        self.all_urls = [url_entry for url_entry in self.all_urls if url_entry is not None]
        
        assert len(self.all_urls) > 0, "No urls fetched on Google search"
        
    def get_url_content(self, url) :
        
        url_entry = {}

        try:
            req = urllib2.Request(url, headers={'User-agent':'Mozilla/5.0'})
            response = urllib2.urlopen(req)
        except Exception:
            return None
            
        url_temp = '/'.join(urlparse.urlparse(url)[2:])
        
        for d in ['$','-', '_', '.', '+', '!', '*', '(', ')', '/',':'] :
            url_temp = url_temp.replace(d, ' ')
            
        url_entry['url'] = url
        url_entry['html'] = response.read() + " " + url_temp
        
        return url_entry
        
    def preprocessQuery(self):
        
        self.keyword = self.keyword.lower()
        
        keywords_all = self.keyword.split();
        
        if self.crawl_topic not in keywords_all:
            keywords_all.append(self.crawl_topic)
            
        self.keyword = ('+').join(keywords_all)