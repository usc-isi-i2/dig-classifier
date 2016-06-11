#!/usr/bin/python

import sys
import json
from preprocessor import Preprocessor
from crawler import Search
from dig_search import Dig_Search
from tfidf_vectorize import Tfidf_Vectorize
from compute_similarity import Similarity
from evaluation import Evaluation
import time
import datetime

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
            print e            
            print "Error in initializing Google search"
        
        t2 = time.time()
        print "Google search done in " + str(t2-t1) + " secs"
        
        # Extract data crawled 
        try :
            crawler.get_crawled_urls()
        except Exception as e :
            print e            
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
        urls_classified = evaluator.compare_similarity(preproc_test)
        
        classified_output = self.formatOutput(urls_classified)
        
        return classified_output
    
    def formatOutput(self,urls_classified) :
        classified_output = []
        
        for url_entry in urls_classified :
            cls_output = {}
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:%S')
            
            cls_output["_index"] = "memex-domains_2014.01"
            cls_output["_type"] = "escorts"
            cls_output["_score"] = url_entry["Similarity_Score"]
            cls_output["_source"] = {}
            cls_output["_source"]["crawl_data"] = {}
            cls_output["_source"]["crawl_data"]["modtime"] = st
            cls_output["_source"]["crawl_data"]["title"] = url_entry['title']
            cls_output["_source"]["crawl_data"]["importtime"] = st
            cls_output["_source"]["url"] = url_entry['Test_url']
            cls_output["_source"]["timestamp"] = ts
            cls_output["_source"]["raw_content"] = url_entry['Raw_Html']
            cls_output["_source"]["content_type"] = "text/html"
            cls_output["_source"]["team"] = "ist"
            
            classified_output.append(cls_output)
        
        return classified_output
            
if __name__ == "__main__" :
    cls = Classifier(sys.argv[1])
    classified_output = cls.classify()
    
    with open("output/"+sys.argv[1]+".json","w") as out :
        out.write(json.dumps(classified_output))





        
    