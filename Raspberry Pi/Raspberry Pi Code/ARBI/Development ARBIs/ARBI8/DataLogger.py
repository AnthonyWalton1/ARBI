#!/usr/bin/env python

class DataLoggerclass(object):
	
	def __init__(self, filename):
		self.filename = filename
		
	def clearFile(self):
		
		open(self.filename, "w").close()
	
	def logData(self, msg):
		
		textFile = open(self.filename, "a")
		textFile.write(msg + "\r\n")
		textFile.close()