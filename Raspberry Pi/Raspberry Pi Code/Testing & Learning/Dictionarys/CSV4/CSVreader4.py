#!/usr/bin/env python

import time
import csv

global timers
global machineState


timers = {}
machineState = {"FCV301" : "0", "V201a" : "0", "V201b" :"0", "V301" : "0", "V302" : "0", "heya" : "1"}

def millis():
	return int(round(time.time() ))	

HATstarttime = millis()
timers["HAT"] = HATstarttime
machineState["FL301"] = 30	
	

class CSVTaskclass:
	
	def __init__(self, csvFilename, stepHeader):
		
		self.csvFilename = csvFilename
		self.stepHeader = stepHeader
		
		self.csvFile = csv.DictReader(open(csvFilename))
		
		self.machineItemsToChange = []
		self.hasMachineStateBeenImplemented = {}
		
		self.csvDict = {}
		
		for self.row in self.csvFile:
			self.key = self.row.pop(self.stepHeader)
			if self.key in self.csvDict:
				pass
			self.csvDict[self.key] = self.row
			
		self.justMeasure = 0
			
	def outputValuesFxn(self, tableStepNumber):
		
		self.tableStepNumber = tableStepNumber
		
		print "4: self.tableStepNumber " + self.tableStepNumber
		
		# Obtain step from table dict
		self.tableStep = self.csvDict[self.tableStepNumber]
		
		
		# Identify which pumps matter 1 or 0 not X (X = don't care)
		for self.machineItem in self.tableStep:
			
			if self.tableStep[self.machineItem] != "X":
				self.machineItemsToChange.append(self.machineItem)
			
		print "5: self.machineItemsToChange " + str(self.machineItemsToChange)
			
		if self.justMeasure == 0:		
			# For all elements that matter send the string to Arduino (how to call UART class)?
			for self.machineItem in self.machineItemsToChange:
				print "6: " + self.machineItem + " " + self.tableStep[self.machineItem]
		
		# Check the values I just sent to current state of machine
		for self.machineItem in self.machineItemsToChange:
			
			if self.tableStep[self.machineItem].split("_")[1] == machineState[self.machineItem]:
				self.hasMachineStateBeenImplemented[self.machineItem] = 1
			else:
				self.hasMachineStateBeenImplemented[self.machineItem] = 0
				
		print "7.1: self.hasMachineStateBeenImplemented " + str(self.hasMachineStateBeenImplemented)
		print "7.2: machineState " + str(machineState)
		
		self.machineItemsToChange = []
		
		if all(self.hasMachineStateBeenImplemented[self.machineItem] == 1 for self.machineItem in self.hasMachineStateBeenImplemented):
			self.justMeasure = 0
			return "complete"
		
		else:
			self.justMeasure = 1
			return "incomplete"
			
		
			





class CSVFlowclass:
	
	def __init__(self, csvFilename, stepHeader, taskClass):
		
		self.csvFilename = csvFilename
		self.stepHeader = stepHeader
		self.taskClass = taskClass
		self.flowChartStep = "1"
		
		self.csvFile = csv.DictReader(open(csvFilename))
		
		self.csvDict = {}
		
		for self.row in self.csvFile:
			self.key = self.row.pop(self.stepHeader)
			if self.key in self.csvDict:
				pass
			self.csvDict[self.key] = self.row



	def printFile(self):
		
		print self.csvDict
		
		
		
	def hasTimePassed(self):
		
		self.timerReference = self.csvDict[self.flowChartStep]["ConditionValues"].split("_")[0]
		self.timewait = self.csvDict[self.flowChartStep]["ConditionValues"].split("_")[1]
		
		self.referenceTime = timers[self.timerReference]
		
		self.timedif = millis() - self.referenceTime
		
		if int(self.timedif) > int(self.timewait):
			
			return "Yes"
			
		else:
			
			return "No"
		
		
		
	def sensorReading(self):
		
		self.sensorID = self.csvDict[self.flowChartStep]["ConditionValues"].split("_")[0]
		self.sensorRequiredValue = self.csvDict[self.flowChartStep]["ConditionValues"].split("_")[1]
			
		self.sensorValue = machineState[self.sensorID]
		print "self.sensorValue" + str(self.sensorValue)
		print "self.sensorRequiredValue" + str(self.sensorRequiredValue)
		
		if int(self.sensorValue) > int(self.sensorRequiredValue):
			
			return "Yes"
			
		else:
			
			return "No"
		
		
		
	def flowChartConditionFxn(self):
	
		if self.csvDict[self.flowChartStep]["ConditionFxn"] == "HasTimePassed":		
			self.flowChartConditionState = self.hasTimePassed()
			print "2: hasTimePassed"
			
		if self.csvDict[self.flowChartStep]["ConditionFxn"] == "SensorReading":	
			self.flowChartConditionState = self.sensorReading()
			print "2: sensorReading"
			
		if self.csvDict[self.flowChartStep]["ConditionFxn"] == "NoCondition":			
			self.flowChartConditionState = "Yes"
			print "2: nocondition"
			
		return self.flowChartConditionState
		

		
		
	def flowChartOperationFxn(self, flowChartConditionState):
		
		self.flowChartConditionState = flowChartConditionState
		print "3: self.flowChartConditionState " + self.flowChartConditionState
			
		if self.flowChartConditionState == "Yes":			
			
			if self.csvDict[self.flowChartStep]["YesOperation"] == "OutputValues":
				self.tableStepNumber = self.csvDict[self.flowChartStep]["YesParameter"]		
				self.outputValuesState = self.taskClass.outputValuesFxn(self.tableStepNumber)

				return self.outputValuesState
				
		if self.flowChartConditionState == "No":

			if self.csvDict[self.flowChartStep]["NoOperation"] == "OutputValues":			
				self.tableStepNumber = self.csvDict[self.flowChartStep]["NoParameter"]				
				self.outputValuesState = self.taskClass.outputValuesFxn(self.tableStepNumber)
				
				return self.outputValuesState
				
			if self.csvDict[self.flowChartStep]["NoOperation"] == "goToAStepInThisFlowChart":
							
				return "complete"
				
	
		
	def doNextStepInFlowChart(self):
		print "1: self.flowChartStep " + self.flowChartStep
		
		self.flowChartConditionState =  self.flowChartConditionFxn()
				
		self.flowChartOperationState = self.flowChartOperationFxn(self.flowChartConditionState)
	
		print "8: self.flowChartOperationState " + str(self.flowChartOperationState)
			
		if self.flowChartOperationState == "complete":
			
			if self.flowChartConditionState == "Yes":			
				self.nextStepInThisFlowChart = self.csvDict[self.flowChartStep]["YesNextStepInThisFlowChart"]
				print "9: self.nextStepInThisFlowChart " + self.nextStepInThisFlowChart
				
				
				if self.nextStepInThisFlowChart != "Finished":
					self.flowChartStep = self.nextStepInThisFlowChart
					return "notfinished"
				else:
					self.flowChartStep = "1"
					return "finished"

			if self.flowChartConditionState == "No":
				self.nextStepInThisFlowChart = self.csvDict[self.flowChartStep]["NoNextStepInThisFlowChart"]
				self.flowChartStep = self.nextStepInThisFlowChart
				print "9: self.nextStepInThisFlowChart " + self.nextStepInThisFlowChart

				if self.nextStepInThisFlowChart != "Finished":
					self.flowChartStep = self.nextStepInThisFlowChart
					return "notfinished"
				else:
					self.flowChartStep = "1"
					
		else:
			print "9: self.nextStepInThisFlowChart " + self.nextStepInThisFlowChart		
			return "repeating"
			
			
				
			
			
taskClass = CSVTaskclass("CSV4Task.csv", "Step")
flow1 = CSVFlowclass("CSV4Flow.csv", "Flow", taskClass)
flow1.printFile()
times = 0

while True:
	times = times + 1
	if times > 1:
		machineState = {"FCV301" : "0", "V201a" : "0", "V201b" :"0", "V301" : "0", "V302" : "0", "heya" : "1", "FL301" : "30"}
	if times > 5:
		machineState = {"FCV301" : "1", "V201a" : "1", "V201b" :"1", "V301" : "1", "V302" : "1", "heya" : "1", "FL301" : "30"}
	if times > 8:
		machineState = {"FCV301" : "1", "V201a" : "0", "V201b" :"1", "V301" : "0", "V302" : "0", "heya" : "1", "FL301" : "200"}
	if times > 9:
		machineState = {"FCV301" : "1", "V201a" : "0", "V201b" :"0", "V301" : "0", "V302" : "0", "heya" : "1", "FL301" : "200"}
	if times > 11:
		machineState = {"FCV301" : "1", "V201a" : "1", "V201b" :"0", "V301" : "0", "V302" : "0", "heya" : "1", "FL301" : "30"}
	if times > 14:
		machineState = {"FCV301" : "1", "V201a" : "1", "V201b" :"0", "V301" : "0", "V302" : "0", "heya" : "1", "FL301" : "10000"}
	if times > 16:
		machineState = {"FCV301" : "1", "V201a" : "0", "V201b" :"0", "V301" : "0", "V302" : "0", "heya" : "1", "FL301" : "10000"}

	
	outcome = flow1.doNextStepInFlowChart()
	print outcome + str(times)
	time.sleep(2)
	
	
	
	
