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

		self.ArbiUART = UART.UARTclass()
				
		# Intialise start-time reference in milliseconds
		self.startTime = millis.millis()
		
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
	
	def feedAlgae(self):
		
		# Start-up check
		if (((self.FMTflag == 0) and ((millis.millis() - self.startTime) > 120 * 1000)) or (self.FATflag == 1)):
			
			if (self.FATflag == 0):
				
				self.FATflag = 1
				self.FATstep = 1
		
		# Set default mode configs first	
		if (self.FATstep == 1):
			
			self.V201b = 0
			self.V301 = 0
			self.V302 = 0
			self.FATstep = 2
		
		# Then set FAT specific configs
		if (self.FATstep == 2):
			
			if ((measurements["V301"] == 0) and (measurements["V302"] == 0) and (measurements["V201b"] == 0)):
				
				self.FCV301 = 1
				self.V201a = 1
				self.FATstep = 3
		
		# Stop FAT specific configs		
		if (self.FATstep == 3):
			
			if measurements["ABLevelSensor"] == 100:
				
				self.V201a = 0
				self.FATstep = 4
		
		# Turn FAT mode off when FAT specific configs are off		
		if (self.FATstep == 4):
			
			if measurements["V201a"] == 0:
				
				self.FATstep = 1
				self.FATflag = 0
		
	def harvestAlgae(self):
	
		if ((millis.millis() - self.startTime) > 600 * 1000):
			
			if (self.HATflag == 0):
			
				self.HATflag = 1
				self.HATstep = 1
				
		if (self.HATstep == 1):
			
			self.PU301 = 0
			self.V304 = 0
			self.V501b = 0
			self.HATstep = 2
			
		if (self.HATstep == 2):
			
			if ((measurements["PU301"] == 0) and (measurements["V304"] == 0) and (measurements["V501b"] == 0)):
				
				self.FCV301 = 1
				self.V201a = 1
				
				
				
			
			
			
			
		
			
			
	
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
