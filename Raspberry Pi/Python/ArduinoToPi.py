#!/usr/bin/env python



import serial

ser = serial.Serial('/dev/ttyACM0', 9600)

while 1:
	print(ser.readline())
	
	
	'''or:
	line = ser.readline()
	
	print(line)
	'''

