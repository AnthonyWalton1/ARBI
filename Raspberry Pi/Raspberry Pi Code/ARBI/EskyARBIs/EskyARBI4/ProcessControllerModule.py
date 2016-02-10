#!/usr/bin/env python

import time
import globalvars
import globalfxns
	
class ProcessControllerClass(object):

	def __init__(self, flowDictionary):
		
		self.flowDictionary = flowDictionary
		
		self.flowChartStep = "1"
		self.componentsToSendInformationFor = []
		self.waitingForHandshake = False
		self.justStarted = True



	def hasTimePassed(self):
		
		self.timerID = self.flowDictionary[self.flowChartStep]["ConditionDescription"] 
		self.timeToWaitSinceReferenceTime = self.flowDictionary[self.flowChartStep]["ConditionValue"]

		self.referenceTime = globalvars.timers[self.timerID]
		
		self.timeElapsedSinceReferenceTime = (globalfxns.millis() - self.referenceTime)/1000
		
		print "ConditionType: hasTimePassed"
		print "referenceTimer: " + str(self.timerID)
		print "timeElapsedSinceReferenceTime: " + str(self.timeElapsedSinceReferenceTime)
		
		if int(self.timeElapsedSinceReferenceTime) > int(self.timeToWaitSinceReferenceTime):
			return "Yes"
		else:
			return "No"
		
		
		
	def sensorReading(self):
		
		self.sensorID = self.flowDictionary[self.flowChartStep]["ConditionDescription"]
		self.sensorRequiredValue = self.flowDictionary[self.flowChartStep]["ConditionValue"]
			
		self.sensorCurrentValue = globalvars.machineState[self.sensorID]

		print "ConditionType: sensorReading"
		print "sensorRequiredValue: " + str(globalvars.machineState[self.sensorID])
		print "sensorCurrentValue: " + str(self.sensorCurrentValue)
		
		if int(self.sensorCurrentValue) > int(self.sensorRequiredValue):
			return "Yes"		
		else:	
			return "No"
			
	
			
	def stateCheck(self):
		
		self.componentsStateCheckOutcomes = {}
		
		self.componentsToStateCheck = self.flowDictionary[self.flowChartStep]["ConditionDescription"].split("&")
		self.componentsDesiredStates = self.flowDictionary[self.flowChartStep]["ConditionValue"].split("&")

		print "ConditionType: stateCheck"
		
		print "self.componentsToStateCheck: " + str(self.componentsToStateCheck)
		
		print "self.componentsDesiredStates: " + str(self.componentsDesiredStates)
		
		self.componentsDesiredStatesIndex = 0
		
		for self.componentID in self.componentsToStateCheck:
			print "self.componentID: " + str(self.componentID)
			print "machineState[self.componentID]: " + str(globalvars.machineState[self.componentID])
			
			if globalvars.machineState[self.componentID] == self.componentsDesiredStates[self.componentsDesiredStatesIndex]:
				self.componentsStateCheckOutcomes[self.componentID] = 1
			else:
				self.componentsStateCheckOutcomes[self.componentID] = 0
				
			self.componentsDesiredStatesIndex += 1
				
		print "self.componentsStateCheckOutcomes: " + str(self.componentsStateCheckOutcomes)
					
		if all(self.componentsStateCheckOutcomes[self.componentID] == 1 for self.componentID in self.componentsStateCheckOutcomes):
			return "Yes"
		else:
			return "No"		
				
		
			
	def determineFlowConditionTypeAndOutcome(self):
	
		if self.flowDictionary[self.flowChartStep]["ConditionType"] == "HasTimePassed":		
			self.flowConditionOutcome = self.hasTimePassed()
			
		if self.flowDictionary[self.flowChartStep]["ConditionType"] == "SensorReading":	
			self.flowConditionOutcome = self.sensorReading()
			
		if self.flowDictionary[self.flowChartStep]["ConditionType"] == "NoCondition":			
			return "Yes"
			
		if self.flowDictionary[self.flowChartStep]["ConditionType"] == "StateCheck":
			self.flowConditionOutcome = self.stateCheck()
			
		return self.flowConditionOutcome
		

		
		
	def performFlowOperation(self, flowConditionOutcome):
		
		self.flowConditionOutcome = flowConditionOutcome
			
		if self.flowConditionOutcome == "Yes":			
			
			if self.flowDictionary[self.flowChartStep]["YesOperation"] == "OutputValues":
				self.taskStep = self.flowDictionary[self.flowChartStep]["YesParameter"]		
				self.flowOperationOutcome = self.outputValuesInTaskStep(self.taskStep)

				return self.flowOperationOutcome
				
		if self.flowConditionOutcome == "No":

			if self.flowDictionary[self.flowChartStep]["NoOperation"] == "OutputValues":			
				self.taskStep = self.flowDictionary[self.flowChartStep]["NoParameter"]	
				self.flowOperationOutcome = self.outputValuesInTaskStep(self.taskStep)
				
				return self.flowOperationOutcome
				
			if self.flowDictionary[self.flowChartStep]["NoOperation"] == "GoToAStepInThisFlowChart":				
				return "Complete"


				
	def outputValuesInTaskStep(self, taskStep):
		
		self.taskStep = taskStep
		
		print "self.taskStep: " + str(self.taskStep)
		
		self.taskStepComponentData = globalvars.taskDictionary[self.taskStep]

		print "self.taskStepComponentData: " + str(self.taskStepComponentData)

		self.componentsToSendInformationFor = []
		
		for self.componentID in self.taskStepComponentData:		
			if self.taskStepComponentData[self.componentID] != "X":
				self.componentsToSendInformationFor.append(self.componentID)
		
		print "self.componentsToSendInformationFor: " + str(self.componentsToSendInformationFor) 
		
		for self.componentID in self.componentsToSendInformationFor:		

			print "globalvars.handshakeMsgReceived just before check: " + str(globalvars.handshakeMsgReceived)

			if bool(globalvars.handshakeMsgReceived[self.componentID]) == False:
				globalvars.GlobalComs.serialWrite(str(globalvars.componentProtocolIDs[self.componentID]) + "_" + str(self.taskStepComponentData[self.componentID]) + "\r\n")
				print "Msg send to Arduino: " + str(globalvars.componentProtocolIDs[self.componentID]) + "_" + str(self.taskStepComponentData[self.componentID]) + "\r\n"
			else:
				globalvars.handshakeMsgReceived[self.componentID] = False	
		
		print "handshakes just before comparison: " + str(globalvars.handshakes)

		if all(globalvars.handshakes[self.componentID] == "1" for self.componentID in self.componentsToSendInformationFor):		
			self.waitingForHandshake = False
			
			for self.componentID in self.componentsToSendInformationFor:	
				globalvars.handshakes[self.componentID] = "0"		
			return "Complete"
		
		else:
			self.waitingForHandshake = True
			
			for self.componentID in self.componentsToSendInformationFor:
				if globalvars.handshakes[self.componentID] == "2":
					print "Error in handshake for " + str(self.componentID)
									
			return "Incomplete"				
				
	
		
	def doNextStepInFlowChart(self):
		
		if self.justStarted == True:
			globalvars.timers["EskyLastStartup"] = globalfxns.millis()			
			self.justStarted = False
		
		if self.waitingForHandshake == False:
			self.flowConditionOutcome =  self.determineFlowConditionTypeAndOutcome()
		
		print "self.flowConditionOutcome: " + str(self.flowConditionOutcome)
				
		self.flowOperationOutcome = self.performFlowOperation(self.flowConditionOutcome)
	
		print "self.flowOperationOutcome: " + str(self.flowOperationOutcome)
			
		if self.flowOperationOutcome == "Complete":	
			
			if self.flowConditionOutcome == "Yes":			
				self.nextStepInThisFlowChart = self.flowDictionary[self.flowChartStep]["YesNextStepInThisFlowChart"]
				
				if self.nextStepInThisFlowChart != "Finished":
					self.flowChartStep = self.nextStepInThisFlowChart
					globalvars.timers["EskySincePreviousYes"] = globalfxns.millis()
					return "Not finished"
				
				else:
					self.flowChartStep = "1"
					globalvars.timers["EskyLastFinish"] = globalfxns.millis()
					self.justStarted = True
					return "Finished"

			if self.flowConditionOutcome == "No":
				self.nextStepInThisFlowChart = self.flowDictionary[self.flowChartStep]["NoNextStepInThisFlowChart"]

				if self.nextStepInThisFlowChart != "Finished":
					self.flowChartStep = self.nextStepInThisFlowChart
					globalvars.timers["EskySincePreviousNo"] = globalfxns.millis()
					return "Not finished"
				
				else:
					self.flowChartStep = "1"
					globalvars.timers["EskyLastFinish"] = globalfxns.millis()
					self.justStarted = True
					return "Finished"
					
		else:
			return "Repeating"
