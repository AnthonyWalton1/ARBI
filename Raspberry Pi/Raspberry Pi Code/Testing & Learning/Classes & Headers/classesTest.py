#!/usr/bin/env python

class printing:
	
	def printplease(self, msg):
		print msg
		return (msg, 2)
		

rpi = printing()
(a, b) = rpi.printplease("Hi",)

print a
print b
