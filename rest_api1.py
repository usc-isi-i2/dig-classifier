# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 12:29:46 2015

@author: gauravsathe
"""

from flask import Flask
from classifier import Classifier
import json

app = Flask("My first app")

@app.route('/')
def api_root() :
	return "Hello World\n"

@app.route('/classifier/<string:search_query>')
def classifier(search_query) :
    cls = Classifier(' '.join(search_query.split('_')))
    classified_output = cls.classify()
    
    if classified_output != None and len(classified_output) > 0 :
        with open("output/" + search_query+".json","w") as out :
            out.write(json.dumps(classified_output))
        
        return json.dumps({"query" : search_query, "status": "Success"})
    else :
        return json.dumps({"query" : search_query, "status": "Failed"})

if __name__ == "__main__" :
    app.run()