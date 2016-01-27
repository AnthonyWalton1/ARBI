#!/usr/bin/env python

# Class definitions
class AI(object):
	
	def status(self):
		print "status"
		
	def bool feedAlgae(self):
		
		feedState = 1;
		
		if (feedStep == 1):
			ser.write("Open valve X\r\n")
			feedStep = 2
			
		if (feedStep == 2):
			if (valveX == "open"):
				ser.write("Turn on pump Y\r\n")
				feedStep = 3
			
		if (feedStep == 3):
			if (waterLevel == 100):
				ser.write("Stop pump Y\r\n")
				feedStep = 4
			
		if (feedStep == 4):
			if (pumpY == "off"):
				ser.write("Close valve X\r\n")
				feedStep = 5			
		
		if (feedStep == 5):
			if (valveX == "closed"):
				algaeFeedTimer =lookupTable.calculate("AlgaeFeed")
				
				feedStep = 1
					
		
		
		
	def harvestAlgae(self):
		print "harvestAlgae"
	
	def harvestRotifers(self):
		print "harvestRotifers"
		
	def probeAlgae(self):
		print "probeAlgae"
		
	def probeRotifers(self):
		print "probeRotifers"
		
	def foodMixing(self):
		print "foddMixing"
		
	def bleachMode(self):
		print "bleachMode"
		
	def bleachAlgaeSafeZone(self):
		print "bleachAlgaeSafeZone"
		
	def bleachRotiferSafeZone(self):
		print "bleachRotiferSafeZone"
		
	def algaeCoulterCounter(self):
		print "algaeCoulterCounter"
		
	def rotiferCoulterCounter(self):
		print "rotiferCoulterCounter"


class Datalogger(object):
	
	def write(self):
		print "write"
	
	
	
# setup
ai = AI();
dataLogger = Datalogger();

	

# mainloop
while 1:
	
	# Measure everything
	ai.status();
	
	# Call courses of action
	ai.feedAlgae();
		
	ai.harvestAlgae();
	
	ai.harvestRotifers();

	ai.probeAlgae();

	ai.probeRotifers();
	
	ai.foodMixing();
	
	ai.bleachMode();
	
	ai.bleachAlgaeSafeZone();
	
	ai.bleachRotiferSafeZone();
	
	ai.algaeCoulterCounter();
	
	ai.rotiferCoulterCounter();
	
	# Write to data logger txt file
	dataLogger.write();
	

	

	
	
	
