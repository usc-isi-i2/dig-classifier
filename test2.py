#!/usr/bin/python

from multiprocessing import Process, Queue

def f(q):
	q.put({'a':1, 'b':2})
	q.put({'c':3, 'd':4})


if __name__ == '__main__':
	q = Queue()
	processes = [Process(target=f, args=(q,)) for i in range(3)]
	
	for p in processes:
		p.start()

	# Exit the completed processes
	for p in processes:
		p.join()

	print q.get()