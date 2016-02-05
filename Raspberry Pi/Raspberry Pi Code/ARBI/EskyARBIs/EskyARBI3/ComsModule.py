#!/usr/bin/env python

# Import headers/modules
import serial
import globalvars
import globalfxns
import time

class ComsClass(object):
	
	serACM0 = serial.Serial("/dev/ttyACM0", 115200)
	serACM1 = serial.Serial("/dev/ttyACM1", 115200)
	
	listACM0 = ["P101", "P102"]
	listACM1 = ["P103"]		
	
	

	def serialWrite(self, text):
		
		if text[0] == "1":
			if text.split("_")[1] in self.listACM0:
				self.serACM0.write(text)
			
			elif text.split("_")[1] in self.listACM1:
				self.serACM1.write(text)
				
		elif text[0] == "2":
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

		if line.split("_")[0] == "1":
			globalvars.handshakes[line.split("_")[1]] = line.split("_")[2]
			globalvars.handshakeMsgReceived[line.split("_")[1]] = True
			
			print "globalvars.handshakeMsgReceived after setting in Coms: " + str(globalvars.handshakeMsgReceived)

		if line.split("_")[0] == "2":
			
			if len(line.split("_")) > 3:
				for i in range(1, ((len(line.split("_")) - 1)/2)+1):
					globalvars.machineState[line.split("_")[2*i-1]] = line.split("_")[2*i]
			
			else:
				globalvars.machineState[line.split("_")[1]] = line.split("_")[2]
