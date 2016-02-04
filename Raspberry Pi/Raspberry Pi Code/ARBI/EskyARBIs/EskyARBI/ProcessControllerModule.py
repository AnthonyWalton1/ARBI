#!/usr/bin/env python

import time
import AIModule
import globalvars
import globalfxns
	
class ProcessControllerClass(object):
	
	def __init__(self, flowDictionary):
		
		self.flowDictionary = flowDictionary
		
		self.flowChartStep = "1"
		self.componentsToSendInformationFor = []
		self.waitingForHandshake = False



	def hasTimePassed(self):
		
		self.timerID = self.flowDictionary[self.flowChartStep]["ConditionDescription"] 
		self.timeToWaitSinceReferenceTime = self.flowDictionary[self.flowChartStep]["ConditionValue"]

		self.referenceTime = globalvars.timers[self.timerID]
		
		self.timeElapsedSinceReferenceTime = (globalfxns.millis() - self.referenceTime)/1000
		
		print "ConditionType: hasTimePassed"
		print "referenceTime: " + str(globalvars.timers[self.timerID])
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
		
		self.stateCheckOutcomes = {}
		
		self.componentIDsToStateCheck = self.flowDictionary["ConditionDescription"].split("&")
		self.componentIDsDesiredStates = self.flowDictionary["ConditionDescription"].split("&")
		
		print self.componentIDsToStateCheck
		print self.componentIDsDesiredStates
		
		self.componentIDsDesiredStatesIndex = 0
		
		for self.componentID in self.componentIDsToStateCheck:
			if machineState[self.componentID] == self.componentIDsDesiredStates[self.componentIDsDesiredStatesIndex]:
				self.stateCheckOutcomes[self.componentID] = 1
			else:
				self.stateCheckOutcomes[self.componentID] = 0
				
		print self.stateCheckOutcomes
					
		if all(self.stateCheckOutcome == 1 for self.stateCheckOutcome in self.stateCheckOutcomes):
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
			if self.waitingForHandshake == False:
				#AIModule.self.Coms.serialWrite(self.componentID + self.taskStepComponentData[self.componentID])
				#AIModule.self.Coms.serialReceive()
				print str(self.componentID) + " " + str(self.taskStepComponentData[self.componentID])
		
			print "handshakes[self.componentID]: " + str(globalvars.handshakes[self.componentID])
		
		if all(globalvars.handshakes[self.componentID] == "1" for self.componentID in self.componentsToSendInformationFor):		
			self.waitingForHandshake = False	
			
			for self.componentID in self.componentsToSendInformationFor:
				globalvars.handshakes[self.componentID] = ""	
			
			return "Complete"
		
		else:
			self.waitingForHandshake = True
			return "Incomplete"				
				
	
		
	def doNextStepInFlowChart(self):
		
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
					
					try:
						print "EskySincePreviousYes before reset: " + str(globalvars.timers["EskySincePreviousYes"])
					
					except:
						a = 1
					
					globalvars.timers["EskySincePreviousYes"] = globalfxns.millis()
					
					print "EskySincePreviousYes after reset: " + str(globalvars.timers["EskySincePreviousYes"])
					return "Not finished"
				
				else:
					self.flowChartStep = "1"
					return "Finished"

			if self.flowConditionOutcome == "No":
				self.nextStepInThisFlowChart = self.flowDictionary[self.flowChartStep]["NoNextStepInThisFlowChart"]

				if self.nextStepInThisFlowChart != "Finished":
					self.flowChartStep = self.nextStepInThisFlowChart
					
					try:
						print "EskySincePreviousNo before reset: " + str(globalvars.timers["EskySincePreviousNo"])
					
					except:
						a = 1
					
					globalvars.timers["EskySincePreviousNo"] = globalfxns.millis()
					
					print "EskySincePreviousNo after reset: " + str(globalvars.timers["EskySincePreviousNo"])
					return "Not finished"
				
				else:
					self.flowChartStep = "1"
					return "Finished"
					
		else:
			return "Repeating"
