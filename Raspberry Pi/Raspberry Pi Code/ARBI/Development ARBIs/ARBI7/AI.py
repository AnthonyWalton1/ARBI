#!/usr/bin/env python

# Import headers/modules
import threading
import GUI
import DataLogger
import UART
import CSVTaskReader
import CSVFlowReader
import GlobalFunctions
import GlobalVariables

class AIclass(object):
	
	def __init__(self):
		
		self.ArbiGUI = GUI.GUIclass("ARBI GUI")
		self.guiThread = threading.Thread(target = self.ArbiGUI.createGUI)
		self.guiThread.start()

		self.ArbiDataLogger = DataLogger.DataLoggerclass("textfile.txt")
		self.ArbiDataLogger.clearFile()

		self.ArbiUART = UART.UARTclass()
		
		self.ArbiCSVTaskReader = CSVTaskReader.CSVTaskReaderclass("CSVTask.csv", "Step")
		GlobalVariables.taskCSVDict = self.ArbiCSVTaskReader.returnTaskDictionary()
		
		self.ArbiCSVFlowReader1 = CSVFlowReader.CSVFlowReaderclass("CSVFlow.csv", "Flow")
				
		# Intialise start-time reference in milliseconds
		GlobalVariables.timers["startTime"] = GlobalFunctions.millis()



	def status(self):
		
		GlobalVariables.machineState["BLED1"] = self.ArbiGUI.getBlueLED1State()

		GlobalVariables.machineState["BLED2"] = self.ArbiGUI.getBlueLED2State()

		GlobalVariables.machineState["BLED3"] = self.ArbiGUI.getBlueLED3State()

		GlobalVariables.machineState["RLED1"] = self.ArbiGUI.getRedLED1State()

		GlobalVariables.machineState["RLED2"] = self.ArbiGUI.getRedLED2State()

		GlobalVariables.machineState["RLED3"] = self.ArbiGUI.getRedLED3State()

		GlobalVariables.machineState["InsideTemp"] = self.ArbiGUI.getInsideTempState()

		GlobalVariables.machineState["WaterTemp"] = self.ArbiGUI.getWaterTempState()

		GlobalVariables.machineState["LEDON"] = self.ArbiGUI.getLedOnTimeState()
		
		GlobalVariables.machineState["LEDOFF"] = self.ArbiGUI.getLedOffTimeState()

		GlobalVariables.machineState["FLASHSTATUS"] = self.ArbiGUI.getFlashStatusState()
		

				
	def decide(self):
		print GlobalVariables.machineState
	
	def feedAlgae(self):
		print "feedalgae"
				
	def harvestAlgae(self):
		print "harvestalgae"
				
	def harvestRotifers(self):
		print "harvestRotifers"
		
	def probeAlgae(self):
		print "probeAlgae"
		
	def probeRotifers(self):
		print "probeRotifers"
		
	def foodMixing(self):
		print "foodMixing"
		
	def bleachMode(self):
		print "bleachMode"
		
	def bleachAlgaeSafeZone(self):
		print "bleachAlgaeSafeZone"
		
	def bleachRotiferSafeZone(self):
		print "bleachRotiferSafeZone"
		
	def rotiferCoulterCounter(self):
		print "rotiferCoulterCounter"
