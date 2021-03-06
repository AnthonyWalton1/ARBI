#!/usr/bin/env python

import time
import csv
import TaskCSV

global taskCSVDict

def millis():
	return int(round(time.time()))	

HATstarttime = millis()
	
timers = {"HAT" : HATstarttime}
machineState = {"FCV301" : "0", "V201a" : "0", "V201b" :"0", "V301" : "0", "V302" : "0", "heya" : "1", "FL301" : 30}



class CSVFlowclass:
	
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
		self.hasMachineStateBeenImplemented = {}
		self.waitingForHandshake = 0

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
		self.tableStep = taskCSVDict[self.tableStepNumber]
		
		for self.machineItem in self.tableStep:		
			if self.tableStep[self.machineItem] != "X":
				self.machineItemsToChange.append(self.machineItem)
			
		for self.machineItem in self.machineItemsToChange:		
			if self.waitingForHandshake == 0:		
				print "6: " + self.machineItem + " " + self.tableStep[self.machineItem]
		
			if self.tableStep[self.machineItem].split("_")[1] == machineState[self.machineItem]:
				self.hasMachineStateBeenImplemented[self.machineItem] = 1
			else:
				self.hasMachineStateBeenImplemented[self.machineItem] = 0
				
		self.machineItemsToChange = []
		
		if all(self.hasMachineStateBeenImplemented[self.machineItem] == 1 for self.machineItem in self.hasMachineStateBeenImplemented):
			self.waitingForHandshake = 0
			return "complete"
		
		else:
			self.waitingForHandshake = 1
			return "incomplete"				
				
	
		
	def doNextStepInFlowChart(self):
	
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
			
			
				
			
			
taskCSVInstance = TaskCSV.TaskCSVclass("CSV5Task.csv", "Step")
taskCSVDict = taskCSVInstance.returnDictOfTaskCSV()
flow1 = CSVFlowclass("CSV5Flow.csv", "Flow")
times = 0

while True:
	times = times + 1
	if times == 2:
		machineState = {"FCV301" : "0", "V201a" : "0", "V201b" :"0", "V301" : "0", "V302" : "0", "heya" : "1", "FL301" : "30"}
	if times == 6:
		machineState = {"FCV301" : "1", "V201a" : "1", "V201b" :"1", "V301" : "1", "V302" : "1", "heya" : "1", "FL301" : "30"}
	if times == 9:
		machineState = {"FCV301" : "1", "V201a" : "0", "V201b" :"1", "V301" : "0", "V302" : "0", "heya" : "1", "FL301" : "200"}
	if times == 10:
		machineState = {"FCV301" : "1", "V201a" : "0", "V201b" :"0", "V301" : "0", "V302" : "0", "heya" : "1", "FL301" : "200"}
	if times == 12:
		machineState = {"FCV301" : "1", "V201a" : "1", "V201b" :"0", "V301" : "0", "V302" : "0", "heya" : "1", "FL301" : "30"}
	if times == 15:
		machineState = {"FCV301" : "1", "V201a" : "1", "V201b" :"0", "V301" : "0", "V302" : "0", "heya" : "1", "FL301" : "10000"}
	if times == 17:
		machineState = {"FCV301" : "1", "V201a" : "0", "V201b" :"0", "V301" : "0", "V302" : "0", "heya" : "1", "FL301" : "10000"}

	
	outcome = flow1.doNextStepInFlowChart()
	print outcome + str(times)
	time.sleep(2)
	
	
	
	
