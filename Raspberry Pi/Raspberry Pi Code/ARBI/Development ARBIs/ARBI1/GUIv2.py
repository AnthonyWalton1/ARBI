#!/usr/bin/env python

from Tkinter import *
import UART

#class GUIclass:
	
#	def __init__(self):
		

def createGUI(mode):
	
	def BlueLed1Set():
	
		input = blueLed1Input.get()
			
		while (len(input) < 5):
			input = "0" + input
				
		print("14_" + input + "\r\n")
		
		UART.serialWrite("14_" + input + "\r\n")
		
		return blueLed1Input.get()
	
	if mode == 1:
		
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

		root.mainloop()
		
	else:
		
		BlueLed1Set()
		
