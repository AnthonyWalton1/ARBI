#!/usr/bin/env python

import csv

class csvReaderclass(object):
	
	def __init__(self, csvFilename, stepHeader):
		
		self.csvFilename = csvFilename
		self.stepHeader = stepHeader
			
	def csvReturnDict(self):
		
		self.csvFile = csv.DictReader(open(self.csvFilename))
		self.csvDict = {}
		
		for self.row in self.csvFile:
			self.key = self.row.pop(self.stepHeader)
			if self.key in self.csvDict:
				pass
			self.csvDict[self.key] = self.row

		return self.csvDict
