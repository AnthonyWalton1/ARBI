#!/usr/bin/env python

from Tkinter import *

import serial
ser = serial.Serial('/dev/ttyACM0', 9600)

import time

class ArbiGUI:
	
	### ************* Attributes & Initial Code ************* ###
	
	def __init__(self, master):
		
		# ***** Code for Resizing GUI ***** #
		
		window.wm_title("ARBI GUI")		
		frame = Frame(master)
		Grid.rowconfigure(master, 0, weight = 1)
		Grid.columnconfigure(master, 0, weight = 1)
		frame.grid(row = 0, column = 0, sticky = N+S+E+W)
		grid = Frame(frame)
		grid.grid(sticky=N+S+E+W, column = 0, row = 7, columnspan = 2)
		Grid.rowconfigure(frame, 7, weight = 1)
		Grid.columnconfigure(frame, 0, weight = 1)

	
		# ***** Led Label Frame ***** #
		
		self.blueLed1Label = Label(frame, text = " Blue LED 1 Intensity:")
		self.blueLed1Label.grid(row = 0, column = 0, sticky = N+S+E+W)
		self.redLed1Label = Label(frame, text = "Red LED 1 Intensity:")
		self.redLed1Label.grid(row = 1, column = 0, sticky = N+S+E+W)

		self.blueLed2Label = Label(frame, text = " Blue LED 2 Intensity:")
		self.blueLed2Label.grid(row = 2, column = 0, sticky = N+S+E+W)
		self.redLed2Label = Label(frame, text = "Red LED 2 Intensity:")
		self.redLed2Label.grid(row = 3, column = 0, sticky = N+S+E+W)
		
		self.blueLed3Label = Label(frame, text = " Blue LED 3 Intensity:")
		self.blueLed3Label.grid(row = 4, column = 0, sticky = N+S+E+W)
		self.redLed3Label = Label(frame, text = "Red LED 3 Intensity:")
		self.redLed3Label.grid(row = 5, column = 0, sticky = N+S+E+W)

		# ***** Current LED values ***** #
		
		self.blueLed1Text = StringVar()
		self.redLed1Text = StringVar()
		self.blueLed2Text = StringVar()
		self.redLed2Text = StringVar()
		self.blueLed3Text = StringVar()
		self.redLed3Text = StringVar()

		self.blueLed1Value = Label(frame, textvariable = self.blueLed1Text, bg = "white")
		self.blueLed1Value.grid(row = 0, column = 1, sticky = N+S+E+W, padx = 20)
		self.redLed1Value = Label(frame, textvariable = self.redLed1Text, bg = "white")
		self.redLed1Value.grid(row = 1, column = 1, sticky = N+S+E+W, padx = 20)

		self.blueLed2Value = Label(frame, textvariable = self.blueLed2Text, bg = "white")
		self.blueLed2Value.grid(row = 2, column = 1, sticky = N+S+E+W, padx = 20)
		self.redLed2Value = Label(frame, textvariable = self.redLed2Text, bg = "white")
		self.redLed2Value.grid(row = 3, column = 1, sticky = N+S+E+W, padx = 20)
		
		self.blueLed3Value = Label(frame, textvariable = self.blueLed3Text, bg = "white")
		self.blueLed3Value.grid(row = 4, column = 1, sticky = N+S+E+W, padx = 20)
		self.redLed3Value = Label(frame, textvariable = self.redLed3Text, bg = "white")
		self.redLed3Value.grid(row = 5, column = 1, sticky = N+S+E+W, padx = 20)
		
		# ***** LED Input Boxes  ***** #
		
		self.blueLed1Input = Entry(frame)
		self.blueLed1Input.grid(row = 0, column = 2, padx = 20)
		self.redLed1Input = Entry(frame)
		self.redLed1Input.grid(row = 1, column = 2, padx = 20)

		self.blueLed2Input = Entry(frame)
		self.blueLed2Input.grid(row = 2, column = 2, padx = 20)
		self.redLed2Input = Entry(frame)
		self.redLed2Input.grid(row = 3, column = 2, padx = 20)
		
		self.blueLed3Input = Entry(frame)
		self.blueLed3Input.grid(row = 4, column = 2, padx = 20)
		self.redLed3Input = Entry(frame)
		self.redLed3Input.grid(row = 5, column = 2, padx = 20)
		
		# ***** LED Enter Buttons ***** #
		
		self.blueLed1Button = Button(frame, text = "Set Blue LED 1 (PWM Ratio/255)", command = self.BlueLed1Enter)
		self.blueLed1Button.grid(row = 0, column = 3, sticky = N+S+E+W)
		self.redLed1Button = Button(frame, text = "Set Red LED 1 (PWM Ratio/255)", command = self.RedLed1Enter)
		self.redLed1Button.grid(row = 1, column = 3, sticky = N+S+E+W)

		self.blueLed2Button = Button(frame, text = "Set Blue LED 2 (PWM Ratio/255)", command = self.BlueLed2Enter)
		self.blueLed2Button.grid(row = 2, column = 3, sticky = N+S+E+W)
		self.redLed2Button = Button(frame, text = "Set Red LED 2 (PWM Ratio/255)", command = self.RedLed2Enter)
		self.redLed2Button.grid(row = 3, column = 3, sticky = N+S+E+W)
		
		self.blueLed3 = Button(frame, text = "Set Blue LED 3 (PWM Ratio/255)", command = self.BlueLed3Enter)
		self.blueLed3.grid(row = 4, column = 3, sticky = N+S+E+W)
		self.redLed3 = Button(frame, text = "Set Red LED 3 (PWM Ratio/255)", command = self.RedLed3Enter)
		self.redLed3.grid(row = 5, column = 3, sticky = N+S+E+W)
		
		# ***** Break Label 1 ***** #
		
		self.BreakLabel1 = Label(frame, text = "------------------------------------------------------------------------------------------------------------------------------------------------")
		self.BreakLabel1.grid(row = 6, columnspan = 4)
		
		# ***** Inside Air Temperature Boxes ***** #
		
		self.insideTempText = StringVar()
		
		self.insideTempLabel = Label(frame, text = " Inside Temperature:")
		self.insideTempLabel.grid(row = 7, column = 0, sticky = N+S+E+W)

		self.insideTempValue = Label(frame, textvariable = self.insideTempText, bg = "white")
		self.insideTempValue.grid(row = 7, column = 1, sticky = N+S+E+W, padx = 20)
		
		self.insideTempInput = Entry(frame)
		self.insideTempInput.grid(row = 7, column = 2, padx = 20)
		
		self.insideTempButton = Button(frame, text = "Set Inside Temperatre (Deg C)", command = self.InsideTempEnter)
		self.insideTempButton.grid(row = 7, column = 3, sticky = N+S+E+W)
		
		# ***** Water Bath Temperature Boxes ***** #
		
		self.waterTempText = StringVar()
		
		self.waterTempLabel = Label(frame, text = " Water Temperature:")
		self.waterTempLabel.grid(row = 8, column = 0, sticky = N+S+E+W)

		self.waterTempValue = Label(frame, textvariable = self.waterTempText, bg = "white")
		self.waterTempValue.grid(row = 8, column = 1, sticky = N+S+E+W, padx = 20)
		
		self.waterTempInput = Entry(frame)
		self.waterTempInput.grid(row = 8, column = 2, padx = 20)
		
		self.waterTempButton = Button(frame, text = " Set Water Temperatre (Deg C)", command = self.WaterTempEnter)
		self.waterTempButton.grid(row = 8, column = 3, sticky = N+S+E+W)
			
		# ***** Break Label 2 ***** #
		
		self.BreakLabel2 = Label(frame, text = "------------------------------------------------------------------------------------------------------------------------------------------------")
		self.BreakLabel2.grid(row = 9, columnspan = 4)
		
		# ***** Frequency Divider 1 Boxes ***** #
		
		self.freqDiv1Text = StringVar()
		
		self.freqDiv1Label = Label(frame, text = " Frequency Divider 1:")
		self.freqDiv1Label.grid(row = 10, column = 0, sticky = N+S+E+W)

		self.freqDiv1Value = Label(frame, textvariable = self.freqDiv1Text, bg = "white")
		self.freqDiv1Value.grid(row = 10, column = 1, sticky = N+S+E+W, padx = 20)
		
		self.freqDiv1Input = Entry(frame)
		self.freqDiv1Input.grid(row = 10, column = 2, padx = 20)
		
		self.freqDiv1Button = Button(frame, text = "Set Frequency Divider 1 ([0, 999])", command = self.freqDiv1Enter)
		self.freqDiv1Button.grid(row = 10, column = 3, sticky = N+S+E+W)
		
		# ***** Frequency Divider 2 Boxes ***** #
		
		self.freqDiv2Text = StringVar()
		
		self.freqDiv2Label = Label(frame, text = " Frequency Divider 2:")
		self.freqDiv2Label.grid(row = 11, column = 0, sticky = N+S+E+W)

		self.freqDiv2Value = Label(frame, textvariable = self.freqDiv2Text, bg = "white")
		self.freqDiv2Value.grid(row = 11, column = 1, sticky = N+S+E+W, padx = 20)
		
		self.freqDiv2Input = Entry(frame)
		self.freqDiv2Input.grid(row = 11, column = 2, padx = 20)
		
		self.freqDiv2Button = Button(frame, text = "Set Frequency Divider 2 ([0, 999])", command = self.freqDiv2Enter)
		self.freqDiv2Button.grid(row = 11, column = 3, sticky = N+S+E+W)
		
		# ***** LED Frequency & Period Display Boxes ***** #
		
		self.freqDisp = StringVar()
		self.periodDisp = StringVar()
		
		self.freqDispTitle = Label(frame, text = "LED Frequency (Hz):")
		self.freqDispTitle.grid(row = 12, column = 0, sticky = N+S+E+W)
		self.periodDispTitle = Label(frame, text = "LED Period (s):")
		self.periodDispTitle.grid(row = 13, column = 0, sticky = N+S+E+W)
		
		self.freqDispLabel = Label(frame, textvariable = self.freqDisp, bg = "white")
		self.freqDispLabel.grid(row = 12, column = 1, sticky = N+S+E+W, padx = 20)
		self.periodDispLabel = Label(frame, textvariable = self.periodDisp, bg = "white")
		self.periodDispLabel.grid(row = 13, column = 1, sticky = N+S+E+W, padx = 20)
		
		# ***** Break Label 3 ***** #
		
		self.BreakLabel2 = Label(frame, text = "------------------------------------------------------------------------------------------------------------------------------------------------")
		self.BreakLabel2.grid(row = 14, columnspan = 4)
		
		# ***** Flow Meter & Average Temperature of Air and Water Display Boxes ***** #
		
		self.flowMeter = StringVar()
		self.averageTemp1 = StringVar()
		self.averageTemp2 = StringVar()
		
		self.flowMeterTitle = Label(frame, text = "Flow Meter (L/min):")
		self.flowMeterTitle.grid(row = 15, column = 0, sticky = N+S+E+W)
		self.averageTemp1Title = Label(frame, text = " Av. Temp. Air (deg C)")
		self.averageTemp1Title.grid(row = 16, column = 0, sticky = N+S+E+W)
		self.averageTemp2Title = Label(frame, text = " Av. Temp. Water (deg C)")
		self.averageTemp2Title.grid(row = 17, column = 0, sticky = N+S+E+W)
		
		self.flowMeterLabel = Label(frame, textvariable = self.flowMeter, bg = "white")
		self.flowMeterLabel.grid(row = 15, column = 1, sticky = N+S+E+W, padx = 20)
		self.averageTemp1Label = Label(frame, textvariable = self.averageTemp1, bg = "white")
		self.averageTemp1Label.grid(row = 16, column = 1, sticky = N+S+E+W, padx = 20)
		self.averageTemp2Label = Label(frame, textvariable = self.averageTemp2, bg = "white")
		self.averageTemp2Label.grid(row = 17, column = 1, sticky = N+S+E+W, padx = 20)
		
		# ***** Break Label 4 ***** #
		
		self.BreakLabel2 = Label(frame, text = "------------------------------------------------------------------------------------------------------------------------------------------------")
		self.BreakLabel2.grid(row = 18, columnspan = 4)
		
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
		
		if (int(self.blueLed1Input.get()) < 10):
			
			print("01_00" + self.blueLed1Input.get() + "\r\n")
			ser.write("01_00" + self.blueLed1Input.get() + "\r\n")
			
		elif (int(self.blueLed1Input.get()) < 100):
			
			print("01_0" + self.blueLed1Input.get() + "\r\n")
			ser.write("01_0" + self.blueLed1Input.get() + "\r\n")
			
		elif (int(self.blueLed1Input.get()) < 256):
			
			print("01_" + self.blueLed1Input.get() + "\r\n")
			ser.write("01_" + self.blueLed1Input.get() + "\r\n")


	def BlueLed2Enter(self):

		if (int(self.blueLed2Input.get()) < 10):
			
			print("02_00" + self.blueLed2Input.get() + "\r\n")
			ser.write("02_00" + self.blueLed2Input.get() + "\r\n")
			
		elif (int(self.blueLed2Input.get()) < 100):
			
			print("02_0" + self.blueLed2Input.get() + "\r\n")
			ser.write("02_0" + self.blueLed2Input.get() + "\r\n")
			
		elif (int(self.blueLed2Input.get()) < 256):
			
			print("02_" + self.blueLed2Input.get() + "\r\n")
			ser.write("02_" + self.blueLed1Input.get() + "\r\n")
			

	def BlueLed3Enter(self):

		if (int(self.blueLed3Input.get()) < 10):
			
			print("03_00" + self.blueLed3Input.get() + "\r\n")
			ser.write("03_00" + self.blueLed3Input.get() + "\r\n")
			
		elif (int(self.blueLed3Input.get()) < 100):
			
			print("03_0" + self.blueLed3Input.get() + "\r\n")
			ser.write("03_0" + self.blueLed3Input.get() + "\r\n")
			
		elif (int(self.blueLed3Input.get()) < 256):
			
			print("03_" + self.blueLed3Input.get() + "\r\n")
			ser.write("03_" + self.blueLed3Input.get() + "\r\n")						
			
		
	def RedLed1Enter(self):
		
		if (int(self.redLed1Input.get()) < 10):
			
			print("04_00" + self.redLed1Input.get() + "\r\n")
			ser.write("04_00" + self.redLed1Input.get() + "\r\n")
			
		elif (int(self.redLed1Input.get()) < 100):
			
			print("04_0" + self.redLed1Input.get() + "\r\n")
			ser.write("04_0" + self.redLed1Input.get() + "\r\n")
			
		elif (int(self.redLed1Input.get()) < 256):
			
			print("04_" + self.redLed1Input.get() + "\r\n")
			ser.write("04_" + self.redLed1Input.get() + "\r\n")
					
	
	def RedLed2Enter(self):

		if (int(self.redLed2Input.get()) < 10):
			
			print("05_00" + self.redLed2Input.get() + "\r\n")
			ser.write("05_00" + self.redLed2Input.get() + "\r\n")
			
		elif (int(self.redLed2Input.get()) < 100):
			
			print("05_0" + self.redLed2Input.get() + "\r\n")
			ser.write("05_0" + self.redLed2Input.get() + "\r\n")
			
		elif (int(self.redLed2Input.get()) < 256):
			
			print("05_" + self.redLed2Input.get() + "\r\n")
			ser.write("05_" + self.redLed2Input.get() + "\r\n")
			
		
	def RedLed3Enter(self):

		if (int(self.redLed3Input.get()) < 10):
			
			print("06_00" + self.redLed3Input.get() + "\r\n")
			ser.write("06_00" + self.redLed3Input.get() + "\r\n")
			
		elif (int(self.redLed3Input.get()) < 100):
			
			print("06_0" + self.redLed3Input.get() + "\r\n")
			ser.write("06_0" + self.redLed3Input.get() + "\r\n")
			
		elif (int(self.redLed3Input.get()) < 256):
			
			print("06_" + self.redLed3Input.get() + "\r\n")
			ser.write("06_" + self.redLed3Input.get() + "\r\n")
			
		
	def InsideTempEnter(self):

		if (int(self.insideTempInput.get()) < 10):
			
			print("07_00" + self.insideTempInput.get() + "\r\n")
			ser.write("07_00" + self.insideTempInput.get() + "\r\n")
			
		elif (int(self.insideTempInput.get()) < 100):
			
			print("07_0" + self.insideTempInput.get() + "\r\n")
			ser.write("07_0" + self.insideTempInput.get() + "\r\n")
			
		elif (int(self.insideTempInput.get()) < 256):
			
			print("07_" + self.insideTempInput.get() + "\r\n")
			ser.write("07_" + self.insideTempInput.get() + "\r\n")
			
	
	def WaterTempEnter(self):

		if (int(self.waterTempInput.get()) < 10):
			
			print("08_00" + self.waterTempInput.get() + "\r\n")
			ser.write("08_00" + self.waterTempInput.get() + "\r\n")
			
		elif (int(self.waterTempInput.get()) < 100):
			
			print("08_0" + self.waterTempInput.get() + "\r\n")
			ser.write("08_0" + self.waterTempInput.get() + "\r\n")
			
		elif (int(self.waterTempInput.get()) < 256):
			
			print("08_" + self.waterTempInput.get() + "\r\n")
			ser.write("08_" + self.waterTempInput.get() + "\r\n")
			
			
	def freqDiv1Enter(self):

		if (int(self.freqDiv1Input.get()) < 10):
			
			print("09_00" + self.freqDiv1Input.get() + "\r\n")
			ser.write("09_00" + self.freqDiv1Input.get() + "\r\n")
			
		elif (int(self.freqDiv1Input.get()) < 100):
			
			print("09_0" + self.freqDiv1Input.get() + "\r\n")
			ser.write("09_0" + self.freqDiv1Input.get() + "\r\n")
			
		elif (int(self.freqDiv1Input.get()) < 1000):
			
			print("09_" + self.freqDiv1Input.get() + "\r\n")
			ser.write("09_" + self.freqDiv1Input.get() + "\r\n")		
			
			
	def freqDiv2Enter(self):

		if (int(self.freqDiv2Input.get()) < 10):
			
			print("10_00" + self.freqDiv2Input.get() + "\r\n")
			ser.write("10_00" + self.freqDiv2Input.get() + "\r\n")
			
		elif (int(self.freqDiv2Input.get()) < 100):
			
			print("10_0" + self.freqDiv2Input.get() + "\r\n")
			ser.write("10_0" + self.freqDiv2Input.get() + "\r\n")
			
		elif (int(self.freqDiv2Input.get()) < 1000):
			
			print("10_" + self.freqDiv2Input.get() + "\r\n")
			ser.write("10_" + self.freqDiv2Input.get() + "\r\n")


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
		
		if len(line) == 90:
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
				self.freqDiv1Text.set(values[8].split("_")[1])
				freqMult1 = 1
			else:
				print("Return string: wrong format 09")
				freqMult1 = 0
				error = 1
							
			if line[65] == "_" and line[62] == " ":
				print("10 correct")
				self.freqDiv2Text.set(values[9].split("_")[1])
				freqMult2 = 1
			else:
				print("Return string: wrong format 10")
				freqMult2 = 0
				error = 1
			
			if line[72] == "_" and line[69] == " ":
				print("11 correct")
				self.flowMeter.set(str(float(values[10].split("_")[1])/10))
			else:
				print("Return string: wrong format 10")
				error = 1
			
			if line[79] == "_" and line[76] == " ":
				print("12 correct")
				self.averageTemp1.set(values[11].split("_")[1])
			else:
				print("Return string: wrong format 11")
				error = 1
				
			if line[86] == "_" and line[83] == " ":
				print("13 correct")
				self.averageTemp2.set(values[12].split("_")[1])
			else:
				print("Return string: wrong format 13")
				error = 1
				
			if freqMult1 == 1 and freqMult2 == 1:
			
				freqDispAns = 2500/(float(self.freqDiv1Text.get()) * float(self.freqDiv2Text.get()))
				periodDispAns = 1/freqDispAns
			
				self.freqDisp.set(str(freqDispAns))
				self.periodDisp.set(str(periodDispAns))	
					
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
