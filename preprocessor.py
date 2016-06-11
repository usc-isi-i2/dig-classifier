#!/usr/bin/python

import json, re
import string
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk import PorterStemmer
from bs4 import BeautifulSoup
import time
from collections import Counter

class Preprocessor:
    """Class to preprocess data"""
    def __init__(self, data):
        self.data = data

    def getStemmedWords(self,html):
        
        stemmed_words=[]
        #stemmer = SnowballStemmer("english")
        stemmer = PorterStemmer()
        for token in html:
            stemmed_words.append(stemmer.stem_word(token))
            
        return ' '.join(stemmed_words)

    def remove_stopwords(self,html) :

        tokens = html.split()
        #stops = stopwords.words('english')
        stops = Counter(stopwords.words('english'))

        html_filtered = [word for word in tokens if stops[word] != 1]

        return html_filtered

    def get_text(self,html) :

        soup = BeautifulSoup(html)
        
        try :        
            page_title = soup.title.string
        except Exception as e:
            page_title = ""
        
        for script in soup(['style', 'script', '[document]', 'head', 'title']) :
            script.extract()

        text = soup.get_text()
        
        text = text.lower().strip(' \t\n\r')
        
        text = text.replace('\t','')
        text = text.replace('\n','')
        text = text.replace('\r','')
        
        text = text.encode(encoding="ascii", errors="ignore")

        return (page_title,text)

    def remove_punctuation(self,html) :

        html_unpunctuated = ""

        for letter in html :
            if letter not in string.punctuation :
                html_unpunctuated += letter

        return html_unpunctuated

    def preprocessor_main(self) :

        data_processed = []
        for index in range(len(self.data)) :
            url = self.data[index]['url']
            html = self.data[index]['html']
            
            title,html_raw,html_stemmed = self.preprocess(html)
            
            if len(html_stemmed) >= 100 :
                self.data[index]['url'] = self.data[index]['url'].encode(encoding='ascii',errors='ignore')
                self.data[index]['html'] = html_stemmed
                self.data[index]['raw_html'] = html_raw
                self.data[index]['title'] = title
                data_processed.append(self.data[index])
        
        self.data = data_processed
        
    def preprocess(self, html) :
        
        page_title,html_text = self.get_text(html)
        
        html_unpunctuated = self.remove_punctuation(html_text)
        
        html_tokenised = self.remove_stopwords(html_unpunctuated)
        
        html_stemmed = self.getStemmedWords(html_tokenised)
        
        html_stemmed = html_stemmed.encode(encoding='ascii', errors='ignore')
        
        return (page_title,html_text,html_stemmed)