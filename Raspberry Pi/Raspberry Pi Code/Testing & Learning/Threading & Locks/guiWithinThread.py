#!/usr/bin/env python

import serial
ser = serial.Serial('/dev/ttyACM0', 9600)
import time
import threading
from Tkinter import *


'''
class GUI(threading.Thread):
	
	def BlueLed1Set(self):
		
		print "Hi from GUI"
	
	def __init__(self):
		threading.Thread.__init__(self)
		root = Tk()
		
		### ***** Code for Resizing GUI ***** ###
				
		root.wm_title("ARBI GUI")		
		frame = Frame(root)
		Grid.rowconfigure(root, 0, weight = 1)
		Grid.columnconfigure(root, 0, weight = 1)
		frame.grid(row = 0, column = 0, sticky = N+S+E+W)
		grid = Frame(frame)
		grid.grid(sticky=N+S+E+W, column = 0, row = 7, columnspan = 2)
		Grid.rowconfigure(frame, 7, weight = 1)
		Grid.columnconfigure(frame, 0, weight = 1)



		### ***** Blue LED 1 Widgets ***** ###

		# Parameter description label (with static text)
		blueLed1Label = Label(frame, text = " Blue LED 1 Intensity (Lux):")
		blueLed1Label.grid(row = 1, column = 0, sticky = N+S+E+W)

		# Current value label (with variable text)
		blueLed1Text = StringVar()
		blueLed1Value = Label(frame, textvariable = blueLed1Text, bg = "white")
		blueLed1Value.grid(row = 1, column = 1, sticky = N+S+E+W, padx = 20)

		# Enter setpoint button
		blueLed1Button = Button(frame, text = "Set Blue LED 1 (PWM Ratio/65535):", command = self.BlueLed1Set)
		blueLed1Button.grid(row = 1, column = 2, sticky = N+S+E+W)

		# Setpoint input entry box (with default value inserted)
		blueLed1Input = Entry(frame)
		blueLed1Input.insert(END, "128")
		blueLed1Input.grid(row = 1, column = 3, padx = 20)
		
		### ***** Rescale GUI size ***** ###
		
		for x in range(4):
			Grid.columnconfigure(frame, x, weight = 1)

		for y in range(22):
			Grid.rowconfigure(frame, y, weight = 1)
			
		root.mainloop()
		
print "hi"

guiThread = GUI()
guiThread.start()

for i in range(1,6):
	time.sleep(1)
	print str(i) + ": hi"

guiThread.join()
'''


def BlueLed1Set():
		
		print "Hi from GUI"

def createGUI():
	
		root = Tk()
		
		### ***** Code for Resizing GUI ***** ###
				
		root.wm_title("ARBI GUI")		
		frame = Frame(root)
		Grid.rowconfigure(root, 0, weight = 1)
		Grid.columnconfigure(root, 0, weight = 1)
		frame.grid(row = 0, column = 0, sticky = N+S+E+W)
		grid = Frame(frame)
		grid.grid(sticky=N+S+E+W, column = 0, row = 7, columnspan = 2)
		Grid.rowconfigure(frame, 7, weight = 1)
		Grid.columnconfigure(frame, 0, weight = 1)



		### ***** Blue LED 1 Widgets ***** ###

		# Parameter description label (with static text)
		blueLed1Label = Label(frame, text = " Blue LED 1 Intensity (Lux):")
		blueLed1Label.grid(row = 1, column = 0, sticky = N+S+E+W)

		# Current value label (with variable text)
		blueLed1Text = StringVar()
		blueLed1Value = Label(frame, textvariable = blueLed1Text, bg = "white")
		blueLed1Value.grid(row = 1, column = 1, sticky = N+S+E+W, padx = 20)

		# Enter setpoint button
		blueLed1Button = Button(frame, text = "Set Blue LED 1 (PWM Ratio/65535):", command = BlueLed1Set)
		blueLed1Button.grid(row = 1, column = 2, sticky = N+S+E+W)

		# Setpoint input entry box (with default value inserted)
		blueLed1Input = Entry(frame)
		blueLed1Input.insert(END, "128")
		blueLed1Input.grid(row = 1, column = 3, padx = 20)
		
		### ***** Rescale GUI size ***** ###
		
		for x in range(4):
			Grid.columnconfigure(frame, x, weight = 1)

		for y in range(22):
			Grid.rowconfigure(frame, y, weight = 1)
			
		root.mainloop()
				
		

time.sleep(1)

print "The program can continue to run while it writes in another thread"
print str(100 + 400)

serThread1 = threading.Thread(target = createGUI)
serThread1.start()

for i in range(1,11):
	print i
	BlueLed1Set()
	time.sleep(1)
	
serThread1.join()
print "Waited until thread was complete"

