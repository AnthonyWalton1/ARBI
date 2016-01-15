#!/usr/bin/env python

'''
from threading import Timer

def hello():
	print("hello")
	t = Timer(1, hello)
	t.start()
	s.cancel()
	
def hi():
	print("hi")
	s = Timer(1.5, hi)
	s.start()
	
t = Timer(1, hello)
s = Timer(1.5, hi)

t.start()
s.start()

for i in range(1, 100000):
	print i
'''

import time

startTime = int(round(time.time()*1000))

def millis():
	return int(round(time.time()*1000)) - startTime;

while 1:
	
	pyTime = millis()
	print pyTime
