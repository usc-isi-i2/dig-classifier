#!/usr/bin/python

import math
import time

class Similarity :
	def __init__(self, doc_train, features_train, docs_test) :
		self.doc_train = doc_train
		self.features_train = features_train
		self.docs_test = docs_test

	def similarity_main(self) :
		
		self.mod_doc_train = self.compute_mod(self.doc_train)

		similarity_per_test_document = []

		for doc in self.docs_test :
			similarity = self.cosine_similarity(doc)
			similarity_per_test_document.append(similarity)
		
		return similarity_per_test_document

	def cosine_similarity(self, doc_test) :
		
		doc_test = dict(doc_test)
		mod_doc_test = self.compute_mod(doc_test)
		features_test = doc_test.keys()
		'''
		similarity_per_train = []

		for (doc_train, mod_doc_train) in self.doc_mod_train :
			doc_train = dict(doc_train)
			
			features_tr = doc_train.keys()
			features_common = set(features_tr) & set(features_test)
			
			similarity = sum([ doc_test[feature] * doc_train[feature] for feature in features_common])
			
			try:
				similarity /= (mod_doc_train * mod_doc_test)
			except ZeroDivisionError:
				similarity /= (1 + (mod_doc_train * mod_doc_test))

			similarity_per_train.append(round(similarity,4))
		'''

		doc_train = dict(self.doc_train)
		
		features_common = set(self.features_train) & set(features_test)
		
		similarity = sum([ doc_test[feature] * doc_train[feature] for feature in features_common])
		
		try:
			similarity /= (self.mod_doc_train * mod_doc_test)
		except ZeroDivisionError:
			similarity /= (1 + (self.mod_doc_train * mod_doc_test))

		return round(similarity, 4)


	def compute_mod(self, doc) :

		#self.doc_mod_train = zip(self.doc_train, [math.sqrt(sum([tfidf**2 for feature,tfidf in dict(doc).iteritems()])) for doc in self.docs_train])
		return math.sqrt(sum([tfidf**2 for feature,tfidf in dict(doc).iteritems()]))