#!/usr/bin/env python

from Tkinter import *

import serial
ser = serial.Serial('/dev/ttyACM0', 9600)

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
		
		self.blueLed1Label = Label(frame, text = "Blue LED 1:")
		self.blueLed1Label.grid(row = 0, column = 0, sticky = N+S+E+W)
		self.redLed1Label = Label(frame, text = "Red LED 1:")
		self.redLed1Label.grid(row = 1, column = 0, sticky = N+S+E+W)

		self.blueLed2Label = Label(frame, text = "Blue LED 2:")
		self.blueLed2Label.grid(row = 2, column = 0, sticky = N+S+E+W)
		self.redLed2Label = Label(frame, text = "Red LED 2:")
		self.redLed2Label.grid(row = 3, column = 0, sticky = N+S+E+W)
		
		self.blueLed3Label = Label(frame, text = "Blue LED 3:")
		self.blueLed3Label.grid(row = 4, column = 0, sticky = N+S+E+W)
		self.redLed3Label = Label(frame, text = "Red LED 3:")
		self.redLed3Label.grid(row = 5, column = 0, sticky = N+S+E+W)

		# ***** Current LED values ***** #

		self.blueLed1Value = Label(frame, text = "100", bg = "white")
		self.blueLed1Value.grid(row = 0, column = 1, sticky = N+S+E+W, padx = 20)
		self.redLed1Value = Label(frame, text = "0", bg = "white")
		self.redLed1Value.grid(row = 1, column = 1, sticky = N+S+E+W, padx = 20)

		self.blueLed2Value = Label(frame, text = "145", bg = "white")
		self.blueLed2Value.grid(row = 2, column = 1, sticky = N+S+E+W, padx = 20)
		self.redLed2Value = Label(frame, text = "20", bg = "white")
		self.redLed2Value.grid(row = 3, column = 1, sticky = N+S+E+W, padx = 20)
		
		self.blueLed3Value = Label(frame, text = "255", bg = "white")
		self.blueLed3Value.grid(row = 4, column = 1, sticky = N+S+E+W, padx = 20)
		self.redLed3Value = Label(frame, text = "201", bg = "white")
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
		
		self.blueLed1Button = Button(frame, text = "Set Blue LED 1 (%)", command = self.BlueLed1Enter)
		self.blueLed1Button.grid(row = 0, column = 3, sticky = N+S+E+W)
		self.redLed1Button = Button(frame, text = "Set Red LED 1 (%)", command = self.RedLed1Enter)
		self.redLed1Button.grid(row = 1, column = 3, sticky = N+S+E+W)

		self.blueLed2Button = Button(frame, text = "Set Blue LED 2 (%)", command = self.BlueLed2Enter)
		self.blueLed2Button.grid(row = 2, column = 3, sticky = N+S+E+W)
		self.redLed2Button = Button(frame, text = "Set Red LED 2 (%)", command = self.RedLed2Enter)
		self.redLed2Button.grid(row = 3, column = 3, sticky = N+S+E+W)
		
		self.blueLed3 = Button(frame, text = "Set Blue LED 3 (%)", command = self.BlueLed3Enter)
		self.blueLed3.grid(row = 4, column = 3, sticky = N+S+E+W)
		self.redLed3 = Button(frame, text = "Set Red LED 3 (%)", command = self.RedLed3Enter)
		self.redLed3.grid(row = 5, column = 3, sticky = N+S+E+W)
		
		
		# ***** Break Label 1 ***** #
		
		self.BreakLabel1 = Label(frame, text = "------------------------------------------------------------------------------------------------------------------------------------------------")
		self.BreakLabel1.grid(row = 6, columnspan = 4)
		
		# ***** Inside Air Temperature Boxes ***** #
		
		self.insideTempLabel = Label(frame, text = "Inside Temperature:")
		self.insideTempLabel.grid(row = 7, column = 0, sticky = N+S+E+W)

		self.insideTempValue = Label(frame, text = "23", bg = "white")
		self.insideTempValue.grid(row = 7, column = 1, sticky = N+S+E+W, padx = 20)
		
		self.insideTempInput = Entry(frame)
		self.insideTempInput.grid(row = 7, column = 2, padx = 20)
		
		self.insideTempButton = Button(frame, text = "Set Inside Temperatre (Deg C)", command = self.InsideTempEnter)
		self.insideTempButton.grid(row = 7, column = 3, sticky = N+S+E+W)
		
		# ***** Water Bath Temperature Boxes ***** #
		
		self.waterTempLabel = Label(frame, text = "Water Temperature:")
		self.waterTempLabel.grid(row = 8, column = 0, sticky = N+S+E+W)

		self.waterTempValue = Label(frame, text = "10", bg = "white")
		self.waterTempValue.grid(row = 8, column = 1, sticky = N+S+E+W, padx = 20)
		
		self.waterTempInput = Entry(frame)
		self.waterTempInput.grid(row = 8, column = 2, padx = 20)
		
		self.waterTempButton = Button(frame, text = " Set Water Temperatre (Deg C)", command = self.WaterTempEnter)
		self.waterTempButton.grid(row = 8, column = 3, sticky = N+S+E+W)
			
		# ***** Break Label 2 ***** #
		
		self.BreakLabel2 = Label(frame, text = "------------------------------------------------------------------------------------------------------------------------------------------------")
		self.BreakLabel2.grid(row = 9, columnspan = 4)
		
		# ***** Frequency Divider 1 Boxes ***** #
		
		self.freqDiv1Label = Label(frame, text = "Frequency Divider 1:")
		self.freqDiv1Label.grid(row = 10, column = 0, sticky = N+S+E+W)

		self.freqDiv1Value = Label(frame, text = "100", bg = "white")
		self.freqDiv1Value.grid(row = 10, column = 1, sticky = N+S+E+W, padx = 20)
		
		self.freqDiv1Input = Entry(frame)
		self.freqDiv1Input.grid(row = 10, column = 2, padx = 20)
		
		self.freqDiv1Button = Button(frame, text = "Set Frequency Divider 1 ([0, 999])", command = self.freqDiv1Enter)
		self.freqDiv1Button.grid(row = 10, column = 3, sticky = N+S+E+W)
		
		# ***** Frequency Divider 2 Boxes ***** #
		
		self.freqDiv2Label = Label(frame, text = "Frequency Divider 2:")
		self.freqDiv2Label.grid(row = 12, column = 0, sticky = N+S+E+W)

		self.freqDiv2Value = Label(frame, text = "999", bg = "white")
		self.freqDiv2Value.grid(row = 12, column = 1, sticky = N+S+E+W, padx = 20)
		
		self.freqDiv2Input = Entry(frame)
		self.freqDiv2Input.grid(row = 12, column = 2, padx = 20)
		
		self.freqDiv2Button = Button(frame, text = "Set Frequency Divider 2 ([0, 999])", command = self.freqDiv2Enter)
		self.freqDiv2Button.grid(row = 12, column = 3, sticky = N+S+E+W)
		
		# ***** Break Label 3 ***** #
		
		self.BreakLabel2 = Label(frame, text = "------------------------------------------------------------------------------------------------------------------------------------------------")
		self.BreakLabel2.grid(row = 13, columnspan = 4)
		
		# ***** Update Current Values Button ***** #
		
		self.updateCurValButton = Button(frame, text = "Update Current Values", command = self.updateCurValEnter)
		self.updateCurValButton.grid(row = 14, column = 0, columnspan = 4, sticky = N+S+E+W)
		
		# ***** Rescale GUI size ***** #
		
		for x in range(4):
			Grid.columnconfigure(frame, x, weight = 1)

		for y in range(15):
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
			
		
	def RedLed1Enter(self):
		
		if (int(self.redLed1Input.get()) < 10):
			
			print("02_00" + self.redLed1Input.get() + "\r\n")
			ser.write("02_00" + self.redLed1Input.get() + "\r\n")
			
		elif (int(self.redLed1Input.get()) < 100):
			
			print("02_0" + self.redLed1Input.get() + "\r\n")
			ser.write("02_0" + self.redLed1Input.get() + "\r\n")
			
		elif (int(self.redLed1Input.get()) < 256):
			
			print("02_" + self.redLed1Input.get() + "\r\n")
			ser.write("02_" + self.redLed1Input.get() + "\r\n")
					
	
	def BlueLed2Enter(self):

		if (int(self.blueLed2Input.get()) < 10):
			
			print("03_00" + self.blueLed2Input.get() + "\r\n")
			ser.write("03_00" + self.blueLed2Input.get() + "\r\n")
			
		elif (int(self.blueLed2Input.get()) < 100):
			
			print("03_0" + self.blueLed2Input.get() + "\r\n")
			ser.write("03_0" + self.blueLed2Input.get() + "\r\n")
			
		elif (int(self.blueLed2Input.get()) < 256):
			
			print("03_" + self.blueLed2Input.get() + "\r\n")
			ser.write("03_" + self.blueLed1Input.get() + "\r\n")
			
		
	def RedLed2Enter(self):

		if (int(self.redLed2Input.get()) < 10):
			
			print("04_00" + self.redLed2Input.get() + "\r\n")
			ser.write("04_00" + self.redLed2Input.get() + "\r\n")
			
		elif (int(self.redLed2Input.get()) < 100):
			
			print("04_0" + self.redLed2Input.get() + "\r\n")
			ser.write("04_0" + self.redLed2Input.get() + "\r\n")
			
		elif (int(self.redLed2Input.get()) < 256):
			
			print("04_" + self.redLed2Input.get() + "\r\n")
			ser.write("04_" + self.redLed2Input.get() + "\r\n")
			
		
	def BlueLed3Enter(self):

		if (int(self.blueLed3Input.get()) < 10):
			
			print("05_00" + self.blueLed3Input.get() + "\r\n")
			ser.write("05_00" + self.blueLed3Input.get() + "\r\n")
			
		elif (int(self.blueLed3Input.get()) < 100):
			
			print("05_0" + self.blueLed3Input.get() + "\r\n")
			ser.write("05_0" + self.blueLed3Input.get() + "\r\n")
			
		elif (int(self.blueLed3Input.get()) < 256):
			
			print("05_" + self.blueLed3Input.get() + "\r\n")
			ser.write("05_" + self.blueLed3Input.get() + "\r\n")
			
		
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
		
		print("Update Current Values")
		ser.write("99_000\r\n")
		
		#while (ser.available == 1):
		
		blueLed1String = ""
		inChar = ser.read()
			
		if (inChar != "\r"):
			blueLed1String += inChar
		
		if (inChar == "\n"):
			v = StringVar()
			self.blueLed1Value(blueLed1String(4) + blueLed1String(5) + blueLed1String(6))
		
		#while (ser.available == 1):
		
		blueLed2String = ""
		inChar = ser.read()
			
		if (inChar != "\r"):
			blueLed2String += inChar
		
		if (inChar == "\r" or "\n"):
			self.blueLed2Value.set(blueLed2String(4) + blueLed2String(5) + blueLed2String(6))
		
		#while (ser.available == 1):
		
		blueLed3String = ""
		inChar = ser.read()
		
		if (inChar != "\r"):
			blueLed3String += inChar
		
		if (inChar == "\r" or "\n"):
			self.blueLed3Value.set(blueLed3String(4) + blueLed3String(5) + blueLed3String(6))			
				
		#while (ser.available == 1):
		
		redLed1String = ""
		inChar = ser.read()
			
		if (inChar != "\r"):
			redLed1String += inChar
		
		if (inChar == "\n"):
			self.redLed1Value.set(redLed1String(4) + redLed1String(5) + redLed1String(6))
				
		#while (ser.available == 1):
		
		redLed2String = ""
		inChar = ser.read()
		
		if (inChar != "\r"):
			redLed2String += inChar
		
		if (inChar == "\n"):
			self.redLed2Value.set(redLed2String(4) + redLed2String(5) + redLed2String(6))
				
		#while (ser.available == 1):
		
		redLed3String = ""
		inChar = ser.read()
			
		if (inChar != "\r"):
			redLed3String += inChar
		
		if (inChar == "\n"):
			self.redLed3Value.set(redLed3String(4) + redLed3String(5) + redLed3String(6))
				
		#while (ser.available == 1):
		
		insideTempString = ""
		inChar = ser.read()
			
		if (inChar != "\r"):
			insideTempString += inChar
		
		if (inChar == "\n"):
			self.insideTempValue.set(insideTempString(4) + insideTempString(5) + insideTempString(6))	
				
		#while (ser.available == 1):
		
		waterTempString = ""
		inChar = ser.read()
			
		if (inChar != "\r"):
			waterTempString += inChar
		
		if (inChar == "\n"):
			self.waterTempValue.set(waterTempString(4) + waterTempString(5) + waterTempString(6))
				
				
																												
window = Tk()

arbi1 = ArbiGUI(window)

window.mainloop()
