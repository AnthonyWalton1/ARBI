#!/usr/bin/env python

class DataLoggerclass:
	
	def __init__(self, filename):
		self.filename = filename
		
	def clearFile(self):
		
		open(self.filename, "w").close()
	
	def logData(self, msg):
		
		text_file = open(self.filename, "a")
		text_file.write(msg + "\r\n")
		text_file.close()
