#!/usr/bin/env python

class DataLoggerClass:
	
	def __init__(self, filename):
		self.filename = filename
		
	def clearFile(self):
		
		open(self.filename, "w").close()
	
	def logData(self, msg):
		
		text_file = open(self.filename, "a")
		
		# Write the data with the correct format into the file
		text_file.write(msg + "\r\n")

		# Close the file each time so that the writing is saved
		text_file.close()
