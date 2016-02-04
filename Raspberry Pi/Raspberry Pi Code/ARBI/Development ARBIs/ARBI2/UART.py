#!/usr/bin/env python

import serial
ser = serial.Serial('/dev/ttyACM0', 9600)

import threading

serialLock = threading.Lock()

def serialWrite(text):

	serialLock.acquire()
	
	ser.write(text)
	
	msgEnd = 0;
	line = ""
		
	while msgEnd == 0:
		if ser.inWaiting() != 0:
			val = ser.read(1)

			if ((val != "\r") and (val != "\n")):
				line += val
					
			if val == "\n":
				msgEnd = 1
				print line + " returned"

	serialLock.release()
	
	return line	
