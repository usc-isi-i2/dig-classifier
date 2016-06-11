#!/usr/bin/python

import sys, json
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy
from collections import Counter
from nltk.corpus import stopwords
import time
import urlparse
from scipy import linalg

def compute_ngrams(text, ngram_range) :

	ngrams = []

	for n in range(ngram_range[0], ngram_range[1]+1) :
		for i in range(0, len(text) - (n-1)) :
			ngrams.append(' '.join(text[i:i+n]))

	return ngrams


class Tfidf_Vectorize :
	def __init__(self, data) :
		self.training_data = data

	def tfidf_vectorize_train(self) :

		corpus = []

		for url_entry in self.training_data :
			corpus.append(url_entry['html'])

		tf = TfidfVectorizer(analyzer='word', ngram_range=(1,2), min_df = 0)

		tfidf_matrix = tf.fit_transform(corpus)

		tfidf_matrix = self.compute_svd(tfidf_matrix.todense())
		#tfidf_matrix = tfidf_matrix.todense()
		self.features_train = tf.get_feature_names()
		self.idf_train = tf.idf_
		self.tfidf_train = [zip(self.features_train,tfidf) for tfidf in tfidf_matrix.tolist()]
		'''
		self.tfidf_train_compressed = []
		for i in range(0, len(self.tfidf_train)) :
			tfidf_vector = []
			for j in range(0, len(self.tfidf_train[i])) :
				if self.tfidf_train[i][j][1] != 0.0 :
					tfidf_vector.append(self.tfidf_train[i][j])
			self.tfidf_train_compressed.append(tfidf_vector)
		'''	

		self.feature_idf_vector = zip(self.features_train, self.idf_train)

		self.tfidf_vector_centroid()

	def tfidf_vector_centroid(self) :

		self.tfidf_centroid_train = [0] * len(self.features_train)

		for index in range(0,len(self.tfidf_train)) :
			for i in range(0, len(self.tfidf_train[index])) :
				self.tfidf_centroid_train[i] += self.tfidf_train[index][i][1]

		self.tfidf_centroid_train = zip(self.features_train, [w/len(self.tfidf_train) for w in self.tfidf_centroid_train])

	def tfidf_vectorize_test(self, test_data) :

		self.test_data = test_data

		corpus = []
		for url_entry in self.test_data :
			corpus.append(url_entry['html'])
		
		self.tfidf_test = []
		self.features_test = set()
		ngram_range = (1,2)
		idf_train = dict(self.feature_idf_vector)

		for doc in corpus :
			normaliseDoc = doc.split()
			doc_features = compute_ngrams(normaliseDoc, ngram_range)
			length = len(doc_features)
			tf = Counter(doc_features)
			
			tfidf_doc = []
			features_current = set(self.features_train)  & set(tf.keys())
			
			for feature in features_current :
				tfidf_doc.append( (feature, (tf[feature] / float(length)) * idf_train[feature]) )
				self.features_test.add(feature)
			
			self.tfidf_test.append(tfidf_doc)
			

	def compute_svd(self, matrix) :
		
		U, sigma, VT = linalg.svd(matrix)

		sigma_prime = linalg.diagsvd(sigma, len(matrix), len(VT))

		tfidf_prime = numpy.dot(numpy.dot(U, sigma_prime), VT)

		return tfidf_prime