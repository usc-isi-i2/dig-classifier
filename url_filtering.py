#!/usr/bin/python

import sys
import json

def url_filtering(urls_input, global_urls_vectorized) :

	urls_and_text = json.loads(open(urls_input, "r").read())
	global_urls_vectorized = json.loads(open(global_urls_vectorized, "r").read())

	urls_vectorized = {}

	for url_entry in urls_and_text :
		if url_entry['url'] in global_urls_vectorized :
			urls_vectorized[url_entry['url']] = global_urls_vectorized[url]
			del urls_and_text[url_entry]

	open(urls,"w").write(json.dumps(urls_and_text))

	return urls_vectorized