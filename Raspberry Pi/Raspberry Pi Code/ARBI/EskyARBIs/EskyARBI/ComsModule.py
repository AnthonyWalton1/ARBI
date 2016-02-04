#!/usr/bin/env python

# Import headers/modules
import serial
import globalvars
import globalfxns

class ComsClass(object):
	
	serACM0 = serial.Serial("/dev/ttyACM0", 9600)
	serACM1 = serial.Serial("/dev/ttyACM1", 9600)
	
	listACM0 = ["a\r\n", "b\r\n", "c\r\n", "ACM0\r\n", "d\r\n"]
	listACM1 = ["A\r\n", "B\r\n", "C\r\n", "ACM1\r\n", "D\r\n"]		
	
	

	def serialWrite(self, text):
		
		if text.split("_")[2] in self.listACM0:
			self.serACM0.write(text)
			
		elif text.split("_")[2] in self.listACM1:
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
		
		if line.split("_")[0] == "1":
			
			ComsVarName = line.split("_")[1]
			ComsVarData = line.split("_")[2]
			
			globalvars.ComsVar[ComsVarName] = ComsVarData
