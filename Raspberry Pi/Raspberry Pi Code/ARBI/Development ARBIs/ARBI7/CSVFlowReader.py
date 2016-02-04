#!/usr/bin/env python

import time
import csv
import CSVTaskReader
import GlobalFunctions
import GlobalVariables


	
class CSVFlowReaderclass:
	
	def __init__(self, csvFilename, stepHeader):
		
		self.csvFilename = csvFilename
		self.stepHeader = stepHeader
		self.flowChartStep = "1"
		
		self.csvFile = csv.DictReader(open(csvFilename))
		
		self.csvDict = {}
		
		for self.row in self.csvFile:
			self.key = self.row.pop(self.stepHeader)
			if self.key in self.csvDict:
				pass
			self.csvDict[self.key] = self.row

		self.machineItemsToChange = []
		self.waitingForHandshake = 0



	def hasTimePassed(self):
		
		self.timerReference = self.csvDict[self.flowChartStep]["ConditionValues"].split("_")[0]
		self.timewait = self.csvDict[self.flowChartStep]["ConditionValues"].split("_")[1]
		
		self.referenceTime = GlobalVariables.timers[self.timerReference]
		
		self.timedif = GlobalFunctions.millis()/1000 - self.referenceTime/1000
		
		print "timer"
		print self.timedif
		print self.timewait
		
		if int(self.timedif) > int(self.timewait):
			return "Yes"
			
		else:
			return "No"
		
		
		
	def sensorReading(self):
		
		self.sensorID = self.csvDict[self.flowChartStep]["ConditionValues"].split("_")[0]
		self.sensorRequiredValue = self.csvDict[self.flowChartStep]["ConditionValues"].split("_")[1]
			
		self.sensorValue = GlobalVariables.machineState[self.sensorID]
		
		print "sensor"
		print self.sensorValue
		print self.sensorRequiredValue
		
		if int(self.sensorValue) > int(self.sensorRequiredValue):
			return "Yes"
			
		else:	
			return "No"
		
		
		
	def flowChartConditionFxn(self):
	
		if self.csvDict[self.flowChartStep]["ConditionFxn"] == "HasTimePassed":		
			self.flowChartConditionState = self.hasTimePassed()
			
		if self.csvDict[self.flowChartStep]["ConditionFxn"] == "SensorReading":	
			self.flowChartConditionState = self.sensorReading()
			
		if self.csvDict[self.flowChartStep]["ConditionFxn"] == "NoCondition":			
			self.flowChartConditionState = "Yes"
			print "nocondition"
			
		return self.flowChartConditionState
		

		
		
	def flowChartOperationFxn(self, flowChartConditionState):
		
		self.flowChartConditionState = flowChartConditionState
			
		if self.flowChartConditionState == "Yes":			
			
			if self.csvDict[self.flowChartStep]["YesOperation"] == "OutputValues":
				self.tableStepNumber = self.csvDict[self.flowChartStep]["YesParameter"]		
				self.outputValuesState = self.outputValuesFxn(self.tableStepNumber)

				return self.outputValuesState
				
		if self.flowChartConditionState == "No":

			if self.csvDict[self.flowChartStep]["NoOperation"] == "OutputValues":			
				self.tableStepNumber = self.csvDict[self.flowChartStep]["NoParameter"]	
				self.outputValuesState = self.outputValuesFxn(self.tableStepNumber)
				
				return self.outputValuesState
				
			if self.csvDict[self.flowChartStep]["NoOperation"] == "goToAStepInThisFlowChart":				
				return "complete"


				
	def outputValuesFxn(self, tableStepNumber):
		
		self.tableStepNumber = tableStepNumber
		self.tableStep = GlobalVariables.taskCSVDict[self.tableStepNumber]

		self.machineItemsToChange = []
		
		for self.machineItem in self.tableStep:		
			if self.tableStep[self.machineItem] != "X":
				self.machineItemsToChange.append(self.machineItem)
			
		for self.machineItem in self.machineItemsToChange:		
			if self.waitingForHandshake == 0:		
				print "6: " + self.machineItem + " " + self.tableStep[self.machineItem]
		
		print "GlobalVariables.handshakes: " + str(GlobalVariables.handshakes)
		
		if all(GlobalVariables.handshakes[self.machineItem] == "1" for self.machineItem in self.machineItemsToChange):
			self.waitingForHandshake = 0
			
			for self.machineItem in self.machineItemsToChange:
				GlobalVariables.handshakes[self.machineItem] = ""
			
			print "GlobalVariables.handshakes: " + str(GlobalVariables.handshakes)
			
			return "complete"
		
		else:
			self.waitingForHandshake = 1
			return "incomplete"				
				
	
		
	def doNextStepInFlowChart(self):
		
		print GlobalVariables.handshakes
	
		if self.waitingForHandshake == 0:
			self.flowChartConditionState =  self.flowChartConditionFxn()
			
		print self.flowChartConditionState
				
		self.flowChartOperationState = self.flowChartOperationFxn(self.flowChartConditionState)
	
		if self.flowChartOperationState == "complete":
			
			if self.flowChartConditionState == "Yes":			
				self.nextStepInThisFlowChart = self.csvDict[self.flowChartStep]["YesNextStepInThisFlowChart"]
				
				if self.nextStepInThisFlowChart != "Finished":
					self.flowChartStep = self.nextStepInThisFlowChart
					return "notfinished"
				else:
					self.flowChartStep = "1"
					return "finished"

			if self.flowChartConditionState == "No":
				self.nextStepInThisFlowChart = self.csvDict[self.flowChartStep]["NoNextStepInThisFlowChart"]

				if self.nextStepInThisFlowChart != "Finished":
					self.flowChartStep = self.nextStepInThisFlowChart
					return "notfinished"
				else:
					self.flowChartStep = "1"
					
		else:
			return "repeating"
				
	
