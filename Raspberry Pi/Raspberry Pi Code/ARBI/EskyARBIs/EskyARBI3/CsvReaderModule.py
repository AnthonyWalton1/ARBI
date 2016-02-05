#!/usr/bin/env python

import csv

class CsvReaderClass(object):
	
	def __init__(self, csvFilename, stepHeader):
		
		self.csvFilename = csvFilename
		self.stepHeader = stepHeader
			
	def csvReturnDict(self):
		
		self.csvFile = csv.DictReader(open(self.csvFilename))
		self.csvDict = {}
		
		for row in self.csvFile:
			key = row.pop(self.stepHeader)
			if key in self.csvDict:
				pass
			self.csvDict[key] = row

		return self.csvDict
