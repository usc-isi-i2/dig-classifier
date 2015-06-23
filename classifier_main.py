#!/usr/bin/python

import sys
import json
import nltk
from url_filtering import url_filtering
from preprocessor import preprocessor

def main(args) :
	
	urls_dig = args[0]
	urls_sourcepin = args[1]

	# Filter out urls which are already vectorized
	urls_dig_vectorized = url_filtering(urls_dig, global_dig_vectorized)
	urls_sourcepin_vectorized = url_filtering(urls_sourcepin, global_sourcepin_vectorized)

	preprocessor(urls_dig)
	preprocessor(urls_sourcepin)

if __name__ == '__main__':
	main(sys.argv[1:])