#!/usr/bin/env python

from Queue import Empty
from ctypes import c_int
from multiprocessing import Process, Queue, Value
from serial import Serial

import time

class Reader:
	def __init__(self, port, baud):
		self.port = Serial(port = port, baudrate = baud)
		
	def __call__(self, *args, **kwargs):
		self.running, self.queue = args
		a = ""
		while self.running.value == 1:
			r = self.port.read()
			if '/r' in r:
				self.queue.put(a)
			else:
				a += r
		print "Reader Ending"
		
		
class Worker:
	def __init(self):
		pass
	
	def __call(self, *args, **kwargs):
		self.running, self.queue = args
		while self.running.value == 1:
			try:
				print self.queue.get_nowait()
			except Empty:
				time.sleep(0.1)
		print "Worker Ending"
		
def main():
	running = Value(c_int, 1)
	readQueue = Queue()
	reader = Process(target = Reader("/dev/ttyUSB0", 9600), args = (running, readQueue))
	worker = Process(target = Worker(), args = (running, readQueue))
	reader.start()
	worker.start()
	time.sleep(5)
	running.value = 0
	reader.join()
	worker.join()
