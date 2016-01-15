#!/usr/bin/env python


# Import required libraries and setup serial com port with Arduino
from Tkinter import *
import serial
import time

'''
while 1:
	time.sleep(3)
	
	ser = serial.Serial('/dev/tty*', 9600)

	print(ser.readline())

	time.sleep(3)

	ser = serial.Serial('/dev/tty*', 9600)

	time.sleep(3)

	print(ser.readline())
'''

while 1:
	time.sleep(3)
	
	ser = serial.Serial('/dev/ttyACM0', 9600)

	ser.write('3')

	time.sleep(3)

	ser = serial.Serial('/dev/ttyACM1', 9600)

	time.sleep(3)

	ser.write('8')
