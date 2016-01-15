#!/usr/bin/env python

# Import headers/modules
import threading
import GUI
import DataLogger
import UART

class AIclass:
	
	def __init__(self, AInumber):
		
		self.AInumber = AInumber
	
		self.ArbiGUI = GUI.GUIclass("ARBI GUI " + self.AInumber)
		self.guiThread = threading.Thread(target = self.ArbiGUI.createGUI)
		self.guiThread.start()

		self.ArbiDataLogger = DataLogger.DataLoggerclass("maintextfile.txt")
		self.ArbiDataLogger.clearFile()

		self.ArbiUART = UART.UARTclass()
		
	def AIlogData(self, text):
		
		self.ArbiDataLogger.logData(text)
		
	def AIserialWrite(self, line):
		
		returnLine = self.ArbiUART.serialWrite(line)
		
		return returnLine
	
	def status(self):
		
		# Use a dictionary (dict) to store values with indexes that can be names
		# This will make it much easier to index as names are meaningful (not jsut 1, 2, 3, ...)
		measurements = {}
		
		measurements["BLED1"] = self.ArbiGUI.getBlueLED1State()

		measurements["BLED2"] = self.ArbiGUI.getBlueLED2State()

		measurements["BLED3"] = self.ArbiGUI.getBlueLED3State()

		measurements["RLED1"] = self.ArbiGUI.getRedLED1State()

		measurements["RLED2"] = self.ArbiGUI.getRedLED2State()

		measurements["RLED3"] = self.ArbiGUI.getRedLED3State()

		measurements["InsideTemp"] = self.ArbiGUI.getInsideTempState()

		measurements["WaterTemp"] = self.ArbiGUI.getWaterTempState()

		measurements["LEDON"] = self.ArbiGUI.getLedOnTimeState()
		
		measurements["LEDOFF"] = self.ArbiGUI.getLedOffTimeState()

		measurements["FLASHSTATUS"] = self.ArbiGUI.getFlashStatusState()
		
		return measurements
				
	def decide(self, measurements):
		
		# Can pass measurements made in status function to the decide function (i.e. the lookup table in here needs this)
		print measurements
	
	def feedAlgae(self):
		print "feedAlgae"
		
	def harvestAlgae(self):
		print "harvestAlgae"
	
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
