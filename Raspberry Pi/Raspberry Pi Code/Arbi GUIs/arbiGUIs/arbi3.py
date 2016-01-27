#!/usr/bin/env python

from Tkinter import *

import serial
ser = serial.Serial('/dev/ttyACM0', 9600)

import time

class ArbiGUI:
	
	### ************* Attributes & Initial Code ************* ###
	
	def __init__(self, master):
		
		# ***** Code for Resizing GUI ***** #
		
		master.wm_title("ARBI GUI")		
		frame = Frame(master)
		Grid.rowconfigure(master, 0, weight = 1)
		Grid.columnconfigure(master, 0, weight = 1)
		frame.grid(row = 0, column = 0, sticky = N+S+E+W)
		grid = Frame(frame)
		grid.grid(sticky=N+S+E+W, column = 0, row = 7, columnspan = 2)
		Grid.rowconfigure(frame, 7, weight = 1)
		Grid.columnconfigure(frame, 0, weight = 1)

		# ***** Title Boxes ***** #
		
		self.parameterLabel = Label(frame, text = "PARAMETERS")
		self.parameterLabel.grid(row = 0, column = 0, sticky = N+S+E+W)
		
		self.measurementLabel = Label(frame, text = "MEASURED VALUE")
		self.measurementLabel.grid(row = 0, column = 1, sticky = N+S+E+W)
		
		self.setpointLabel = Label(frame, text = "SETPOINT VALUES")
		self.setpointLabel.grid(row = 0, column = 2, sticky = N+S+E+W)
		
		self.enterButtonsLabel = Label(frame, text = "ENTER SETPOINTS")
		self.enterButtonsLabel.grid(row = 0, column = 3, sticky = N+S+E+W)

	
		# ***** Led Label Frame ***** #
		
		self.blueLed1Label = Label(frame, text = " Blue LED 1 Intensity (Lux):")
		self.blueLed1Label.grid(row = 1, column = 0, sticky = N+S+E+W)
		self.redLed1Label = Label(frame, text = "Red LED 1 Intensity (Lux):")
		self.redLed1Label.grid(row = 2, column = 0, sticky = N+S+E+W)

		self.blueLed2Label = Label(frame, text = " Blue LED 2 Intensity (Lux):")
		self.blueLed2Label.grid(row = 3, column = 0, sticky = N+S+E+W)
		self.redLed2Label = Label(frame, text = "Red LED 2 Intensity (Lux):")
		self.redLed2Label.grid(row = 4, column = 0, sticky = N+S+E+W)
		
		self.blueLed3Label = Label(frame, text = " Blue LED 3 Intensity (Lux):")
		self.blueLed3Label.grid(row = 5, column = 0, sticky = N+S+E+W)
		self.redLed3Label = Label(frame, text = "Red LED 3 Intensity (Lux):")
		self.redLed3Label.grid(row = 6, column = 0, sticky = N+S+E+W)

		# ***** Current LED values ***** #
		
		self.blueLed1Text = StringVar()
		self.redLed1Text = StringVar()
		self.blueLed2Text = StringVar()
		self.redLed2Text = StringVar()
		self.blueLed3Text = StringVar()
		self.redLed3Text = StringVar()

		self.blueLed1Value = Label(frame, textvariable = self.blueLed1Text, bg = "white")
		self.blueLed1Value.grid(row = 1, column = 1, sticky = N+S+E+W, padx = 20)
		self.redLed1Value = Label(frame, textvariable = self.redLed1Text, bg = "white")
		self.redLed1Value.grid(row = 2, column = 1, sticky = N+S+E+W, padx = 20)

		self.blueLed2Value = Label(frame, textvariable = self.blueLed2Text, bg = "white")
		self.blueLed2Value.grid(row = 3, column = 1, sticky = N+S+E+W, padx = 20)
		self.redLed2Value = Label(frame, textvariable = self.redLed2Text, bg = "white")
		self.redLed2Value.grid(row = 4, column = 1, sticky = N+S+E+W, padx = 20)
		
		self.blueLed3Value = Label(frame, textvariable = self.blueLed3Text, bg = "white")
		self.blueLed3Value.grid(row = 5, column = 1, sticky = N+S+E+W, padx = 20)
		self.redLed3Value = Label(frame, textvariable = self.redLed3Text, bg = "white")
		self.redLed3Value.grid(row = 6, column = 1, sticky = N+S+E+W, padx = 20)
		
		# ***** LED Input Boxes  ***** #
		
		self.blueLed1Input = Entry(frame)
		self.blueLed1Input.insert(END, "128")
		self.blueLed1Input.grid(row = 1, column = 3, padx = 20)
		self.redLed1Input = Entry(frame)
		self.redLed1Input.insert(END, "128")
		self.redLed1Input.grid(row = 2, column = 3, padx = 20)

		self.blueLed2Input = Entry(frame)
		self.blueLed2Input.insert(END, "128")
		self.blueLed2Input.grid(row = 3, column = 3, padx = 20)
		self.redLed2Input = Entry(frame)
		self.redLed2Input.insert(END, "128")
		self.redLed2Input.grid(row = 4, column = 3, padx = 20)
		
		self.blueLed3Input = Entry(frame)
		self.blueLed3Input.insert(END, "128")
		self.blueLed3Input.grid(row = 5, column = 3, padx = 20)
		self.redLed3Input = Entry(frame)
		self.redLed3Input.insert(END, "128")
		self.redLed3Input.grid(row = 6, column = 3, padx = 20)
		
		# ***** LED Enter Buttons ***** #
		
		self.blueLed1Button = Button(frame, text = "Set Blue LED 1 (PWM Ratio/255):", command = self.BlueLed1Enter)
		self.blueLed1Button.grid(row = 1, column = 2, sticky = N+S+E+W)
		self.redLed1Button = Button(frame, text = "Set Red LED 1 (PWM Ratio/255):", command = self.RedLed1Enter)
		self.redLed1Button.grid(row = 2, column = 2, sticky = N+S+E+W)

		self.blueLed2Button = Button(frame, text = "Set Blue LED 2 (PWM Ratio/255):", command = self.BlueLed2Enter)
		self.blueLed2Button.grid(row = 3, column = 2, sticky = N+S+E+W)
		self.redLed2Button = Button(frame, text = "Set Red LED 2 (PWM Ratio/255):", command = self.RedLed2Enter)
		self.redLed2Button.grid(row = 4, column = 2, sticky = N+S+E+W)
		
		self.blueLed3Button = Button(frame, text = "Set Blue LED 3 (PWM Ratio/255):", command = self.BlueLed3Enter)
		self.blueLed3Button.grid(row = 5, column = 2, sticky = N+S+E+W)
		self.redLed3Button = Button(frame, text = "Set Red LED 3 (PWM Ratio/255):", command = self.RedLed3Enter)
		self.redLed3Button.grid(row = 6, column = 2, sticky = N+S+E+W)
		
		# ***** Break Label 1 ***** #
		
		breakLabel = ""
		
		while len(breakLabel) < 200:
			breakLabel += "-"
		
		self.BreakLabel1 = Label(frame, text = breakLabel)
		self.BreakLabel1.grid(row = 7, columnspan = 4)
		
		# ***** Inside Air Temperature Boxes ***** #
		
		self.insideTempText = StringVar()
		
		self.insideTempLabel = Label(frame, text = " Inside Temperature (deg C):")
		self.insideTempLabel.grid(row = 8, column = 0, sticky = N+S+E+W)

		self.insideTempValue = Label(frame, textvariable = self.insideTempText, bg = "white")
		self.insideTempValue.grid(row = 8, column = 1, sticky = N+S+E+W, padx = 20)
		
		self.insideTempInput = Entry(frame)
		self.insideTempInput.insert(END, "23")
		self.insideTempInput.grid(row = 8, column = 3, padx = 20)
		
		self.insideTempButton = Button(frame, text = "Set Inside Temperatre (deg C):", command = self.InsideTempEnter)
		self.insideTempButton.grid(row = 8, column = 2, sticky = N+S+E+W)
		
		# ***** Water Bath Temperature Boxes ***** #
		
		self.waterTempText = StringVar()
		
		self.waterTempLabel = Label(frame, text = " Water Temperature (deg C):")
		self.waterTempLabel.grid(row = 9, column = 0, sticky = N+S+E+W)

		self.waterTempValue = Label(frame, textvariable = self.waterTempText, bg = "white")
		self.waterTempValue.grid(row = 9, column = 1, sticky = N+S+E+W, padx = 20)
		
		self.waterTempInput = Entry(frame)
		self.waterTempInput.insert(END, "10")
		self.waterTempInput.grid(row = 9, column = 3, padx = 20)
		
		self.waterTempButton = Button(frame, text = " Set Water Temperatre (deg C):", command = self.WaterTempEnter)
		self.waterTempButton.grid(row = 9, column = 2, sticky = N+S+E+W)
			
		# ***** Break Label 2 ***** #
		
		self.BreakLabel2 = Label(frame, text = breakLabel)
		self.BreakLabel2.grid(row = 10, columnspan = 4)
		
		# ***** LED on time Boxes ***** #
		
		self.ledOnTimeText = StringVar()
		
		self.ledOnTimeLabel = Label(frame, text = " LED on time (sec):")
		self.ledOnTimeLabel.grid(row = 11, column = 0, sticky = N+S+E+W)

		self.ledOnTimeValue = Label(frame, textvariable = self.ledOnTimeText, bg = "white")
		self.ledOnTimeValue.grid(row = 11, column = 1, sticky = N+S+E+W, padx = 20)
		
		self.ledOnTimeInput = Entry(frame)
		self.ledOnTimeInput.insert(END, "1")
		self.ledOnTimeInput.grid(row = 11, column = 3, padx = 20)
		
		self.ledOnTimeButton = Button(frame, text = "Set LED on time (sec):", command = self.ledOnTimeEnter)
		self.ledOnTimeButton.grid(row = 11, column = 2, sticky = N+S+E+W)
		
		# ***** LED off time boxes ***** #
		
		self.ledOffTimeText = StringVar()
		
		self.ledOffTimeLabel = Label(frame, text = " LED off time (sec):")
		self.ledOffTimeLabel.grid(row = 12, column = 0, sticky = N+S+E+W)

		self.ledOffTimeValue = Label(frame, textvariable = self.ledOffTimeText, bg = "white")
		self.ledOffTimeValue.grid(row = 12, column = 1, sticky = N+S+E+W, padx = 20)
		
		self.ledOffTimeInput = Entry(frame)
		self.ledOffTimeInput.insert(END, "1")
		self.ledOffTimeInput.grid(row = 12, column = 3, padx = 20)
		
		self.ledOffTimeButton = Button(frame, text = "Set LED off time (sec):", command = self.ledOffTimeEnter)
		self.ledOffTimeButton.grid(row = 12, column = 2, sticky = N+S+E+W)
		
		# ***** LED permanent settings on/off/flash Radio Buttons ***** #
		
		self.radioVar = StringVar()
		
		self.ledOffTimeLabel = Label(frame, text = " LED Mode:")
		self.ledOffTimeLabel.grid(row = 13, column = 0, sticky = N+S+E+W)
		
		self.ledOnRadio = Radiobutton(frame, text = "Set LEDs on", variable = self.radioVar, value = "1", command = self.radioEnter)
		self.ledOnRadio.grid(row = 13, column = 1, sticky = N+S+E+W)
		
		self.ledOffRadio = Radiobutton(frame, text = "Set LEDs off", variable = self.radioVar, value = "2", command = self.radioEnter)
		self.ledOffRadio.grid(row = 13, column = 3, sticky = N+S+E+W)
		
		self.ledFlashRadio = Radiobutton(frame, text = "Set LEDs flash", variable = self.radioVar, value = "0", command = self.radioEnter)
		self.ledFlashRadio.grid(row = 13, column = 2, sticky = N+S+E+W)
		
		
		# ***** Break Label 3 ***** #
		
		self.BreakLabel2 = Label(frame, text = breakLabel)
		self.BreakLabel2.grid(row = 14, columnspan = 4)
		
		# ***** Flow Meter & Average Temperature of Air and Water Display Boxes ***** #
		
		self.flowMeter = StringVar()
		self.averageTemp1 = StringVar()
		self.averageTemp2 = StringVar()
		
		self.flowMeterTitle = Label(frame, text = "Flow Meter (L/min):")
		self.flowMeterTitle.grid(row = 15, column = 0, sticky = N+S+E+W)
		self.averageTemp1Title = Label(frame, text = " Av. Temp. Air (deg C):")
		self.averageTemp1Title.grid(row = 16, column = 0, sticky = N+S+E+W)
		self.averageTemp2Title = Label(frame, text = " Av. Temp. Water (deg C):")
		self.averageTemp2Title.grid(row = 17, column = 0, sticky = N+S+E+W)
		
		self.flowMeterLabel = Label(frame, textvariable = self.flowMeter, bg = "white")
		self.flowMeterLabel.grid(row = 15, column = 1, sticky = N+S+E+W, padx = 20)
		self.averageTemp1Label = Label(frame, textvariable = self.averageTemp1, bg = "white")
		self.averageTemp1Label.grid(row = 16, column = 1, sticky = N+S+E+W, padx = 20)
		self.averageTemp2Label = Label(frame, textvariable = self.averageTemp2, bg = "white")
		self.averageTemp2Label.grid(row = 17, column = 1, sticky = N+S+E+W, padx = 20)
		
		# ***** Break Label 4 ***** #

		self.BreakLabel2 = Label(frame, text = breakLabel)
		self.BreakLabel2.grid(row = 18, columnspan = 4, sticky  = N+S+E+W)
		
		# ***** Update Current Values Button ***** #
		
		self.updateCurValButton = Button(frame, text = "Update Current Values", command = self.updateCurValEnter)
		self.updateCurValButton.grid(row = 19, column = 0, columnspan = 4, sticky = N+S+E+W)
		
		# ***** Rescale GUI size ***** #
		
		for x in range(4):
			Grid.columnconfigure(frame, x, weight = 1)

		for y in range(20):
			Grid.rowconfigure(frame, y, weight = 1)
			
		
	### ******************   Methods   ****************** ###
		
	def BlueLed1Enter(self):
		
		input = self.blueLed1Input.get()
		
		while (len(input) < 3):
			input = "0" + input
			
		print("01_" + input + "\r\n")
		ser.write("01_" + input + "\r\n")	


	def BlueLed2Enter(self):

		input = self.blueLed2Input.get()
		
		while (len(input) < 3):
			input = "0" + input
			
		print("02_" + input + "\r\n")
		ser.write("02_" + input + "\r\n")	
			

	def BlueLed3Enter(self):

		input = self.blueLed3Input.get()
		
		while (len(input) < 3):
			input = "0" + input
			
		print("03_" + input + "\r\n")
		ser.write("03_" + input + "\r\n")							
			
		
	def RedLed1Enter(self):
		
		input = self.redLed1Input.get()
		
		while (len(input) < 3):
			input = "0" + input
			
		print("04_" + input + "\r\n")
		ser.write("04_" + input + "\r\n")	
					
	
	def RedLed2Enter(self):

		input = self.redLed2Input.get()
		
		while (len(input) < 3):
			input = "0" + input
			
		print("05_" + input + "\r\n")
		ser.write("05_" + input + "\r\n")	
			
		
	def RedLed3Enter(self):
		
		input = self.redLed3Input.get()
		
		while (len(input) < 3):
			input = "0" + input
			
		print("06_" + input + "\r\n")
		ser.write("06_" + input + "\r\n")	
			
		
	def InsideTempEnter(self):

		input = self.insideTempInput.get()
		
		while (len(input) < 3):
			input = "0" + input
			
		print("07_" + input + "\r\n")
		ser.write("07_" + input + "\r\n")	
			
	
	def WaterTempEnter(self):

		input = self.waterTempInput.get()
		
		while (len(input) < 3):
			input = "0" + input
			
		print("08_" + input + "\r\n")
		ser.write("08_" + input + "\r\n")	
			
			
	def ledOnTimeEnter(self):
		
		input = str(int(float(self.ledOnTimeInput.get()) * 1000))
		
		while (len(input) < 8):
			input = "0" + input
			
		input = self.radioVar.get() + input	
		print("09_" + input + "\r\n")
		ser.write("09_" + input + "\r\n")	
		
			
	def ledOffTimeEnter(self):

		input = str(int(float(self.ledOffTimeInput.get()) * 1000))
		
		while (len(input) < 8):
			input = "0" + input
		
		input = self.radioVar.get() + input		
		print("10_" + input + "\r\n")
		ser.write("10_" + input + "\r\n")
	
		
	def radioEnter(self):
		
		self.ledOnTimeEnter()
		self.ledOffTimeEnter()	


	def updateCurValEnter(self):
		
		# Send signal to Arduino to send its current values
		ser.write("99_000\r\n")
		
		# Wait for 1 second for Arduino to calculate and send information
		time.sleep(1)
		
		# Read one byte at a time as it is received
		val = ser.read(1)

		# Initialise an empty string
		line = ""
		
		# The signal for end of transmission is an enter (\r\n)
		# Note: this sequence prevents the last character '\r' from being included in the string
		while val not in ["\n"]:
		
			if val != "\r":
				
				# While the signal has not ended, add each byte to the next spot in the string
				line += val
			
			# Read the next byte
			val = ser.read(1)

		# Split the incoming string at the spaces as each data piece is separated by a space
		values = line.split(" ")
		
		print(line)
		
		# The first piece of data corresponds to Blue Led 1 so index values at 0.
		# Then, split this at the underscore and take the second element that is the value (i.e. index 1)
		# The first value is a number that signals what parameter the value relates to (i.e for Blue Led, signal = 01)
		
		# Repeat for all, setting the new value shown in the label boxes
		
		# Include error checking that checks that the indexed element will actually exist based on split
		# Note: the final enter \r\n isn't included in calculating len(line)
		
		# Reset error flag to off
		error = 0
		
		print(len(line))
		if len(line) == 102:
			print("correct length")
			
			if line[2] == "_":
				print("01 correct")
				self.blueLed1Text.set(values[0].split("_")[1])
			else:
				print("Return string: wrong format 01")
				error = 1
			
			if line[9] == "_" and line[6] == " ":
				print("02 correct")
				self.blueLed2Text.set(values[1].split("_")[1])
			else:
				print("Return string: wrong format 02")
				error = 1
			
			if line[16] == "_" and line[13] == " ":
				print("03 correct")
				self.blueLed3Text.set(values[2].split("_")[1])
			else:
				print("Return string: wrong format 03")
				error = 1
			
			if line[23] == "_" and line[20] == " ":
				print("04 correct")
				self.redLed1Text.set(values[3].split("_")[1])
			else:
				print("Return string: wrong format 04")
				error = 1
			
			if line[30] == "_" and line[27] == " ":
				print("05 correct")
				self.redLed2Text.set(values[4].split("_")[1])
			else:
				print("Return string: wrong format 05")
				error = 1
			
			if line[37] == "_" and line[34] == " ":
				print("06 correct")
				self.redLed3Text.set(values[5].split("_")[1])
			else:
				print("Return string: wrong format 06")
				error = 1		
			
			if line[44] == "_" and line[41] == " ":
				print("07 correct")
				self.insideTempText.set(values[6].split("_")[1])
			else:
				print("Return string: wrong format 07")
				error = 1
							
			if line[51] == "_" and line[48] == " ":
				print("08 correct")
				self.waterTempText.set(values[7].split("_")[1])
			else:
				print("Return string: wrong format 08")
				error = 1
							
			if line[58] == "_" and line[55] == " ":
				print("09 correct")
				if (self.radioVar.get() == "0"):
					self.ledOnTimeText.set(values[8].split("_")[1])
				elif (self.radioVar.get() == "1"):
					self.ledOnTimeText.set("On")
				else:
					self.ledOnTimeText.set("Off")
			else:
				print("Return string: wrong format 09")
				error = 1
							
			if line[71] == "_" and line[68] == " ":
				print("10 correct")
				if (self.radioVar.get() == "0"):
					self.ledOffTimeText.set(values[9].split("_")[1])
				elif (self.radioVar.get() == "1"):
					self.ledOffTimeText.set("On")
				else:
					self.ledOffTimeText.set("Off")
			else:
				print("Return string: wrong format 10")
				error = 1
			
			if line[84] == "_" and line[81] == " ":
				print("11 correct")
				self.flowMeter.set(str(float(values[10].split("_")[1])/10))
			else:
				print("Return string: wrong format 10")
				error = 1
			
			if line[91] == "_" and line[88] == " ":
				print("12 correct")
				self.averageTemp1.set(values[11].split("_")[1])
			else:
				print("Return string: wrong format 11")
				error = 1
				
			if line[98] == "_" and line[95] == " ":
				print("13 correct")
				self.averageTemp2.set(values[12].split("_")[1])
			else:
				print("Return string: wrong format 13")
				error = 1
					
		else:
			print("Return string: wrong length")
			error = 1
			
			
		# If any errors occured, request a resend	
		if error == 1:
			# Send signal to Arduino to send its current values again
			ser.write("99_000\r\n")
		
		
		
# Start a new GUI																												
window = Tk()

# Create an instance of the class called arbi1
arbi1 = ArbiGUI(window)

# Run the GUI until quitting
window.mainloop()
