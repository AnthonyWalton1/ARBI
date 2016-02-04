#!/usr/bin/env python

# Import headers/modules
import threading
import GUI
import DataLogger
import UART
import millis

class AIclass:
	
	def __init__(self, AInumber):
		
		self.AInumber = AInumber
	
		self.ArbiGUI = GUI.GUIclass("ARBI GUI " + self.AInumber)
		self.guiThread = threading.Thread(target = self.ArbiGUI.createGUI)
		self.guiThread.start()

		self.ArbiDataLogger = DataLogger.DataLoggerclass("maintextfile.txt")
		self.ArbiDataLogger.clearFile()

		self.ArbiUARTACM0 = UART.UARTclass("/dev/ttyACM0", 9600)
		self.ArbiUARTACM1 = UART.UARTclass("/dev/ttyACM1", 9600)
				
		# Intialise start-time reference in milliseconds
		self.startTime = millis.millis()
		
	def AIlogData(self, text):
		
		self.ArbiDataLogger.logData(text)
		
	def AIserialWriteACM0(self, line):
		
		self.ArbiUARTACM0.serialWrite(line)
	
	def AIserialReceiveACM0(self):
		
		returnLine = self.ArbiUARTACM0.serialReceive()
		
		return returnLine	

	def AIserialWriteACM1(self, line):
		
		self.ArbiUARTACM1.serialWrite(line)
	
	def AIserialReceiveACM1(self):
		
		returnLine = self.ArbiUARTACM1.serialReceive()
		
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
		print measurements
	
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
