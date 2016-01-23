#!/usr/bin/env python

def zero():
	print "zero"
	
def sqr():
	print "square"
	
def even():
	print "even"
	
def prime():
	print "prime"

options = {0 : zero, 3 : prime, 1 : sqr, 2 : even}

options[3]()
options[0]()
options[2]()
options[1]()
