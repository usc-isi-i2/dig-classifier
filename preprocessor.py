#!/usr/bin/python

import json
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from bs4 import BeautifulSoup

def getStemmedWords(html_tokenised):
	
	stemmed_words=[]
	stemmer = SnowballStemmer("english")
	
	for token in html_tokenised:
		stemmed_words.append(stemmer.stem(token))

	return stemmed_words

def remove_stopwords(html) :

	tokens = html.split()

	html_filtered = [word for word in tokens if word not in stopwords.words('english')]

def get_text(html) :

	soup = BeautifulSoup(html)

	text = soup.get_text().lower()

	text = text.replace('\n',' ')

	return text

def preprocessor(urls_input) :

	urls_and_text = json.loads(open(urls_input, "r").read())

	for url_entry in urls_and_text :
		url = url_entry['url']
		html = url_entry['html']

		html_text = get_text(html)
		
		html_tokenised = remove_stopwords(html_text)

		html_stemmed = getStemmedWords(html_tokenised)

	for host in hosts :
		urls_for_host = json.loads(open("urls_per_host/"+host,"r").read())
		
		for url_entry in urls_for_host :
			url = url_entry['url']
			#title = url_entry['title']
			html = url_entry['html']

			if compute_relevance(url,html,query) == True :
				classified_output.write(url+","+"true"+"\n")
				count_true += 1
			else :
				classified_output.write(url+","+"false"+"\n")
 				count_false += 1
