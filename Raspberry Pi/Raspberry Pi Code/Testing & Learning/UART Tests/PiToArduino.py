#!/usr/bin/env python


import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600)
ser.write('3')

time.sleep(1)

ser.write('9')

time.sleep(10)

ser.write('1')

