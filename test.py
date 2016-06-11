import signal
import time

def pre(preproc_test) :
	signal.signal(signal.SIGALRM, signal_handler)

	data_processed = []
	t0 = time.time()
	for index in range(len(preproc_test.data)) :
		t1 = time.time()	
		url = preproc_test.data[index]['url']
		html = preproc_test.data[index]['html']
		
		html_text = preproc_test.get_text(html)
		t2 = time.time()
		print "Get text :" + str(t2-t1)
		signal.alarm(1)
		try :
			html_normalised = dummy(index)#preproc_test.normalize_text(html_text)
		except Exception :
			print "time out"
			continue
		finally :
			signal.alarm(0)

		t3 = time.time()
		print "Normalize :" + str(t3-t2)
		html_unpunctuated = preproc_test.remove_punctuation(html_normalised)
		t4 = time.time()
		print "Remove punc :" + str(t4-t3)
		html_tokenised = preproc_test.remove_stopwords(html_unpunctuated)
		t5 = time.time()
		print "Stopwords :" + str(t5-t4)
		html_stemmed = preproc_test.getStemmedWords(html_tokenised)
		t6 = time.time()
		print "Stemming : " + str(t6-t5)
		html_stemmed = html_stemmed.encode(encoding='ascii', errors='ignore')

		if len(html_stemmed) >= 100 :
			preproc_test.data[index]['url'] = preproc_test.data[index]['url'].encode(encoding='ascii',errors='ignore')
			preproc_test.data[index]['html'] = html_stemmed
			data_processed.append(preproc_test.data[index])

	preproc_test.data = data_processed

	t7 = time.time()
	print ">>>>>>>>All done in " + str(t7-t0)

def signal_handler() :
	raise Exception

def dummy(index) :
	
	if index == 8 :
		dummy2()
				
	return "hello world"

def dummy2() :
	while(1) :
		pass
