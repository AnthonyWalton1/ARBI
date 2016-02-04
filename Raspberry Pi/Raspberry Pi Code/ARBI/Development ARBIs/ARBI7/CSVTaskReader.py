#!/usr/bin/env python

import csv

class CSVTaskReaderclass:
	
	def __init__(self, csvFilename, stepHeader):
		
		self.csvFilename = csvFilename
		self.stepHeader = stepHeader
		
		self.csvFile = csv.DictReader(open(csvFilename))
		
		self.csvDict = {}
		
		for self.row in self.csvFile:
			self.key = self.row.pop(self.stepHeader)
			if self.key in self.csvDict:
				pass
			self.csvDict[self.key] = self.row
			
	def returnTaskDictionary(self):
		
		return self.csvDict
