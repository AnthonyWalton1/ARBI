#!/usr/bin/env python

import Queue
import threading
import time
import urllib2

# Part 1:
'''
import thread
import time

def print_time(threadName, delay):
	count = 0
	while count < 5:
		time.sleep(delay)
		count += 1
		print "%s: %s" % (threadName, time.ctime(time.time()))
		
try:
	thread.start_new_thread(print_time, ("Thread-1", 0.5))
	thread.start_new_thread(print_time, ("Thread-2", 1))
except:
	print "Error: unable to start thread"
	
while 1:
	pass
'''

'''
# Part 2:

def do_stuff(q):
	while not q.empty():
		print q.get()
		time.sleep(1)
		q.task_done()
		
q = Queue(maxsize = 0)

for x in range(20):
	q.put(x)

do_stuff(q)
'''

'''
# Part 3:

def do_stuff(q):
	while True:
		print q.get()
		q.task_done()
		
q = Queue(maxsize=0)
num_threads = 10

for i in range(num_threads):
	worker = threading.Thread(target = do_stuff, args = (q,))
	worker.setDaemon(True)
	worker.start()
	
for x in range(20):
	q.put(x)

q.join()
'''

'''
# Part 4:

def get_url(q, url):
	q.put(urllib2.urlopen(url).read())
	
theurls = ["http://google.com", "http://yahoo.com"]

q = Queue.Queue()

for u in theurls:
	t = threading.Thread(target = get_url, args = (q, u))
	t.daemon = True
	t.start()
	
s = q.get()
print s
'''

# Part 5:

class AsyncWrite(threading.Thread):
	def __init__(self, text, out):
		threading.Thread.__init__(self)
		self.text = text
		self.out = out
		
	def run(self):
		f = open(self.out, "a")
		f.write(self.text + '\n')
		f.close()
		time.sleep(2)
		print "Finished Background file write to" + self.out
		
		
def Main():
	message = raw_input("Enter a string to store")
	background = AsyncWrite(message, "out.txt")
	backgrond.start()
	print "The program can continue to run while it writes in another thread"
	print str(100 + 400)
	
	background.join()
	print "Waited until thread was complete"
	
if __name == "__main__":
	Main()



# Part 6:













