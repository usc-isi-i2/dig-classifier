#!/usr/bin/python

import re
import matplotlib.pyplot as plt
import numpy

def compute_dev(test) :
	dev_pos = []
	dev_neg = []

	pos_full = False
	neg_full = False

	for entry in test :
		if pos_full == False and re.search(r'.*diego.*escort.*',entry['html']) != None :
			dev_pos.append(entry)
			if len(dev_pos) % 5 == 0 :
				print "Pos :", len(dev_pos)
		elif neg_full == False :
			dev_neg.append(entry)
			if len(dev_neg) % 5 == 0:
				print "Neg :", len(dev_neg)
		if len(dev_neg) == 10 :
			neg_full = True
		if len(dev_pos) == 40 :
			pos_full = True
			break

	return (dev_pos, dev_neg)

def similarity_mean(sim) :
	# Compute average of similarity values in sim. Subtract 1 to remove similarity of a url with itself.
	return (sum(sim) - 1)/len(sim)

class Evaluation:
    def __init__(self, sim_train, sim_test) :
        self.sim_train = sim_train
        self.sim_test = sim_test

    def compare_similarity(self, preproc_test) :
        
        sim_count = zip(range(0,len(self.sim_test)), self.sim_test)
        sim_count = sorted(sim_count, key=lambda t:t[1], reverse=True)
        
        avg_train_similarity = numpy.mean(self.sim_train)
        epsilon = 0.4 * avg_train_similarity
        
        urls_classified = []
        
        for sim in sim_count :
            if sim[1] >= (avg_train_similarity-epsilon) :
                url_desc = {}
                url_desc['Test_url'] = preproc_test.data[sim[0]]['url']                
                url_desc['Classifier_Output'] = True
                
                url_desc['Similarity_Score'] = sim[1]
                
                url_desc['Raw_Html'] = preproc_test.data[sim[0]]['raw_html']
                url_desc['title'] = preproc_test.data[sim[0]]['title']
                urls_classified.append(url_desc)
        
        return urls_classified
