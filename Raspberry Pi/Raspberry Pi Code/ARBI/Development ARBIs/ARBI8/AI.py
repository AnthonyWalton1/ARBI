#!/usr/bin/env python

# Import headers/modules
import threading
import GUI
import DataLogger
import UART
import csvReader
import csvInterpreter
import globalfxns
import globalvars

class AIclass(object):
	
	def __init__(self):
		
		self.ArbiGUI = GUI.GUIclass("ARBI GUI")
		self.guiThread = threading.Thread(target = self.ArbiGUI.createGUI)
		self.guiThread.start()

		self.ArbiDataLogger = DataLogger.DataLoggerclass("textfile.txt")
		self.ArbiDataLogger.clearFile()

		self.ArbiUART = UART.UARTclass()
		
		self.ArbiTaskReader = csvReader.csvReaderclass("CSVTask.csv", "Step")
		globalvars.taskDictionary = self.ArbiTaskReader.csvReturnDict()

		self.ArbiFeedAlgaeReader = csvReader.csvReaderclass("CSVFlow.csv", "Flow")
		self.feedAlgaeDictionary = self.ArbiFeedAlgaeReader.csvReturnDict()

		self.ArbiFeedAlgaeInterpreter = csvInterpreter.csvInterpreterclass(self.feedAlgaeDictionary)	
				
		# Intialise start-time reference in milliseconds
		globalvars.timers["startTime"] = globalfxns.millis()



	def status(self):
		
		globalvars.machineState["BLED1"] = self.ArbiGUI.getBlueLED1State()

		globalvars.machineState["BLED2"] = self.ArbiGUI.getBlueLED2State()

		globalvars.machineState["BLED3"] = self.ArbiGUI.getBlueLED3State()

		globalvars.machineState["RLED1"] = self.ArbiGUI.getRedLED1State()

		globalvars.machineState["RLED2"] = self.ArbiGUI.getRedLED2State()

		globalvars.machineState["RLED3"] = self.ArbiGUI.getRedLED3State()

		globalvars.machineState["InsideTemp"] = self.ArbiGUI.getInsideTempState()

		globalvars.machineState["WaterTemp"] = self.ArbiGUI.getWaterTempState()

		globalvars.machineState["LEDON"] = self.ArbiGUI.getLedOnTimeState()
		
		globalvars.machineState["LEDOFF"] = self.ArbiGUI.getLedOffTimeState()

		globalvars.machineState["FLASHSTATUS"] = self.ArbiGUI.getFlashStatusState()
		

				
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