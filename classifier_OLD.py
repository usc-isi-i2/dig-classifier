#!/usr/bin/python

import sys
import json
import nltk
from preprocessor import Preprocessor
from crawler import Search
from dig_search import Dig_Search
from tfidf_vectorize import Tfidf_Vectorize
from compute_similarity import Similarity
from evaluation import Evaluation
import numpy
import time
from json2html import *
from collections import OrderedDict

class Classifier :
    """Classifier to extract urls based on query"""
    
    def __init__(self,query) :
        assert (query != None and query != '' and query.isspace() == False), "Invalid search query. Please enter a valid query"
        
        self.search_query = query
    
    def classify(self) :
        t1 = time.time()
        
        # Schedule a crawl job with the query
        try :        
            crawler = Search(self.search_query)
            crawler.googleSearch()
        except Exception as e :
            print "Error in initializing Google search"
        
        t2 = time.time()
        print "Google search done in " + str(t2-t1) + " secs"
        
        # Extract data crawled 
        try :
            crawler.get_crawled_urls()
        except Exception as e :
            print "Error in extracting crawl data"
        
        t3 = time.time()
        print "Test data extraction done in " + str(t3-t2) + " secs"
        
        # Preprocess test data
        try :
            preproc_test = Preprocessor(crawler.all_urls)
            preproc_test.preprocessor_main()
        except Exception as e :
            print e
            print "Error in preprocessing crawl data"
            
        t4 = time.time()
        print "Test data preprocessing done in " + str(t4-t3) + " secs"
        
        # Send a search request to Dig server with the query
        dig_search = Dig_Search(self.search_query)
        dig_search.search_request()
        t5 = time.time()
        print "Dig Search done in " + str(t5-t4) + " secs"
        
        # Extract results returned by search query
        dig_search.dig_extraction()
        t6 = time.time()
        print "Dig extraction done in " + str(t6-t5) + " secs"
        
        # Preprocess the search results
        try :        
            preproc_train = Preprocessor(dig_search.urls_dig)
            preproc_train.preprocessor_main()
            dig_search.filter_dig_result(preproc_train.data)
        except Exception as e :
            print e
            print "Error in preprocessing training data"
            
        t7 = time.time()
        print "Training data preprocessing done in " + str(t7-t6) + " secs"
        
        # Compute tfidf vectors of data
        try :        
            tfidf_train = Tfidf_Vectorize(dig_search.urls_dig)
            tfidf_train.tfidf_vectorize_train()
            tfidf_train.tfidf_vectorize_test(preproc_test.data)
        except Exception as e :
            print e
            print "Error in computing tfidf vectorization"
        
        t9 = time.time()
        print "Tfidf computation done in " + str(t9-t7) + " secs"
        
        # Compute similarity of training data with its centroid vector
        try :        
            sim_train = Similarity(tfidf_train.tfidf_centroid_train, tfidf_train.features_train, tfidf_train.tfidf_train)
            similarity_train = sim_train.similarity_main()
        except Exception as e :
            print e
            print "Error in computing cosine similarity"
            
        t10 = time.time()
        print "Training data similarity computation done in " + str(t10-t9) + " secs"
        
        # Compute similarity of test data with training data
        try :        
            sim_test = Similarity(tfidf_train.tfidf_centroid_train, tfidf_train.features_train, tfidf_train.tfidf_test)
            similarity_test = sim_test.similarity_main()
        except Exception as e :
            print e
            print "Error in computing cosine similarity"
            
        t11 = time.time()
        print "Similarity computation done in " + str(t11-t10) + " secs"
        
        print "Total time = " + str(t11-t1)
        
        evaluator = Evaluation(similarity_train, similarity_test)
        similarity_count = evaluator.compare_similarity(preproc_test)
        
        avg_train_similarity = numpy.mean(similarity_train)
        epsilon = 0.4 * avg_train_similarity
        classifier_output = open("output/" + self.search_query.replace(' ','_') + "2.html","w")
        urls_classified = []
        
        tfidf_tr = tfidf_train.tfidf_centroid_train
        tfidf_tr = sorted(tfidf_tr, key= lambda tfidf : tfidf[1], reverse=True)
        
        for sim in similarity_count :
            url_desc = {}
            url_desc['Test_url'] = "<a href='"+preproc_test.data[sim[0]]['url']+"''>"+preproc_test.data[sim[0]]['url']+"</a>"
            if sim[1] >= (avg_train_similarity-epsilon) :
                url_desc['Classifier Output'] = True
            else :
                url_desc['Classifier Output'] = False
            
            url_desc['Similarity Score'] = sim[1]
            url_desc['Average Training Similarity'] = avg_train_similarity
            
            tfidf_url = tfidf_train.tfidf_test[sim[0]]
            tfidf_url = sorted(tfidf_url, key= lambda tfidf : tfidf[1], reverse=True)
            
            url_desc['Top Test Keywords'] = ", ".join([tfidf[0] for tfidf in tfidf_url[0:20]])
            urls_classified.append(url_desc)
            
        _json2conv = {"" : urls_classified}
        classifier_output.write("<html><h2 align='center' style='text-decoration:underline'>Classifier Output</h3><h2 align='center'>Query : "+self.search_query+"</h2><h2 align='center'>Top Train Keywords : "+", ".join([tfidf[0] for tfidf in tfidf_tr[0:20]])+"</h2><body>"+ json2html.convert(json=_json2conv, table_attributes="border=2, cellspacing=0, cellpadding=5, text-align='center'") + "</body></html>")
        
        classifier_output.close()
        
if __name__ == "__main__" :
    cls = Classifier(sys.argv[1])
    cls.classify()





        
    