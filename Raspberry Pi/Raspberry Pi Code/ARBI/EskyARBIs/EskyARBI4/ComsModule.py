#!/usr/bin/env python

# Import headers/modules
import serial
import globalvars
import globalfxns
import time

class ComsClass(object):
	
	serACM0 = serial.Serial("/dev/ttyACM0", 115200)
	serACM1 = serial.Serial("/dev/ttyACM1", 115200)
	
	listACM0 = ["001", "002"]
	listACM1 = ["003"]		
	
	

	def serialWrite(self, text):
		
		if len(text) == 7:
			if text.split("_")[0] in self.listACM0:
				self.serACM0.write(text)
			
			elif text.split("_")[0] in self.listACM1:
				self.serACM1.write(text)
				
		elif len(text) == 3:
			self.serACM0.write(text)
			time.sleep(1)
			self.serACM1.write(text)		
			


	def serialReceive(self):

		lineACM0 = ""
		lineACM1 = ""
			
		while self.serACM0.inWaiting() != 0:
			val = self.serACM0.read(1)

			if ((val != "\r") and (val != "\n")):
				lineACM0 += val
					
			if val == "\n":
				self.serialSort(lineACM0)
				lineACM0 = ""
					
		while self.serACM1.inWaiting() != 0:
			val = self.serACM1.read(1)

			if ((val != "\r") and (val != "\n")):
				lineACM1 += val
					
			if val == "\n":
				self.serialSort(lineACM1)
				lineACM1 = ""				


	
	def serialSort(self, line):
		
		print "line: " + str(line)
		
		# This is returning a handshake
		if len(line) == 7:
			globalvars.handshakes[globalvars.componentProtocolIDs[line.split("_")[0]]] = line.split("_")[2]
			globalvars.handshakeMsgReceived[globalvars.componentProtocolIDs[line.split("_")[0]]] = True
			
			print "globalvars.handshakeMsgReceived after setting in Coms: " + str(globalvars.handshakeMsgReceived)
		
		# This is a machine state data packet
		elif len(line) == 5 or len(line) == 11:
			
			globalvars.machineState[globalvars.componentProtocolIDs[line.split("_")[0]]] = line.split("_")[1]
			
