#!/usr/bin/env python

# Import headers/modules
import serial
ser = serial.Serial("/dev/ttyACM0", 9600)
import threading

#global machineState
#global handshakes

class UARTclass:

	
	def __init__(self, port, baud):
		self.port = port
		self.baud = baud		
		self.ser = serial.Serial(port=self.port, baudrate=self.baud)
		
	
	def serialWrite(self, text):
		
		self.text = text

		self.ser.write(self.text)

	def serialReceive(self):

		self.msgEnd = 0;
		self.line = ""
			
		while self.msgEnd == 0:
			if self.ser.inWaiting() != 0:
				self.val = self.ser.read(1)

				if ((self.val != "\r") and (self.val != "\n")):
					self.line += self.val
						
				if self.val == "\n":
					self.msgEnd = 1
					print self.line + " returned from" + self.port

		return self.line + " returned from" + self.port
		'''
	def serialSort(self, string):
		
		self.string = string
		
		if self.string[1] == "1":
			self.handshakeData = string.split("_")
			self.handshakes[handshakeData[0]] = self.handshakeData[1]
		
		elif self.string[1] == "2":
			self.machineStateData = string.split("_")
			
			for 
		'''
		
		
