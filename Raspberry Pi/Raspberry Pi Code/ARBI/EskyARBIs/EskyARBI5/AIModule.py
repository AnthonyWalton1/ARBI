#!/usr/bin/env python

# Import headers/modules
import threading
import GUIModule
import DataLoggerModule
import CsvReaderModule
import ProcessControllerModule
import globalfxns
import globalvars

class AIClass(object):
	
	def __init__(self):
		
		# Create GUI object and assign to its own thread
		self.GUI = GUIModule.GUIClass("ARBI GUI")
		self.GUIThread = threading.Thread(target = self.GUI.createGUI)
		self.GUIThread.start()

		# Create data logger object and clear previous file
		self.DataLogger = DataLoggerModule.DataLoggerClass("textfile.txt")
		self.DataLogger.clearFile()
		
		# Create CSV Reader objects for as many csv files as there is to read
		self.StepReader = CsvReaderModule.CsvReaderClass("taskEskyValidated.csv", "Task")
		globalvars.taskDictionary = self.StepReader.csvReturnDict()

		self.EskyReader = CsvReaderModule.CsvReaderClass("flowEskyValidated.csv", "Flow")
		self.eskyDictionary = self.EskyReader.csvReturnDict()

		# Create Task Controller objects for as many flow chart dictionaries as there is to implement
		self.EskyController = ProcessControllerModule.ProcessControllerClass(self.eskyDictionary, "2")	
				
		# Intialise starting time references in milliseconds
		globalvars.timers["EskySinceLastStartup"] = globalfxns.millis()



	def status(self):
		
		globalvars.machineState["BLED1"] = self.GUI.getBlueLED1State()

		globalvars.machineState["BLED2"] = self.GUI.getBlueLED2State()

		globalvars.machineState["BLED3"] = self.GUI.getBlueLED3State()

		globalvars.machineState["RLED1"] = self.GUI.getRedLED1State()

		globalvars.machineState["RLED2"] = self.GUI.getRedLED2State()

		globalvars.machineState["RLED3"] = self.GUI.getRedLED3State()

		globalvars.machineState["InsideTemp"] = self.GUI.getInsideTempState()

		globalvars.machineState["WaterTemp"] = self.GUI.getWaterTempState()

		globalvars.machineState["LEDON"] = self.GUI.getLedOnTimeState()
		
		globalvars.machineState["LEDOFF"] = self.GUI.getLedOffTimeState()

		globalvars.machineState["FLASHSTATUS"] = self.GUI.getFlashStatusState()
				
	def decide(self):
		print globalvars.machineState
	
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
