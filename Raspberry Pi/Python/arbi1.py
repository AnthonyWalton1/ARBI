#!/usr/bin/env python

from Tkinter import *

class ArbiGUI:
	
	def __init__(self, master):
		
		### ************* Attributes & Initial Code ************* ###
		
		# ***** Led Label Frame ***** #
		
		self.BlueLed1Label = Label(master, text = "Blue LED 1")
		self.BlueLed1Label.grid(row = 0, column = 0, sticky = W)
		self.RedLed1Label = Label(master, text = "Red LED 1")
		self.RedLed1Label.grid(row = 1, column = 0, sticky = W)

		self.BlueLed2Label = Label(master, text = "Blue LED 2")
		self.BlueLed2Label.grid(row = 2, column = 0, sticky = W)
		self.RedLed2Label = Label(master, text = "Red LED 2")
		self.RedLed2Label.grid(row = 3, column = 0, sticky = W)
		
		self.BlueLed3Label = Label(master, text = "Blue LED 3")
		self.BlueLed3Label.grid(row = 4, column = 0, sticky = W)
		self.RedLed3Label = Label(master, text = "Red LED 3")
		self.RedLed3Label.grid(row = 5, column = 0, sticky = W)

		# ***** Current LED values ***** #

		self.BlueLed1Value = Label(master, text = "100", bg = "white")
		self.BlueLed1Value.grid(row = 0, column = 1, sticky = W, padx = 20)
		self.RedLed1Value = Label(master, text = "0", bg = "white")
		self.RedLed1Value.grid(row = 1, column = 1, sticky = W, padx = 20)

		self.BlueLed2Value = Label(master, text = "145", bg = "white")
		self.BlueLed2Value.grid(row = 2, column = 1, sticky = W, padx = 20)
		self.RedLed2Value = Label(master, text = "20", bg = "white")
		self.RedLed2Value.grid(row = 3, column = 1, sticky = W, padx = 20)
		
		self.BlueLed3Value = Label(master, text = "255", bg = "white")
		self.BlueLed3Value.grid(row = 4, column = 1, sticky = W, padx = 20)
		self.RedLed3Value = Label(master, text = "201", bg = "white")
		self.RedLed3Value.grid(row = 5, column = 1, sticky = W, padx = 20)
		
		# ***** LED Input Boxes  ***** #
		
		self.BlueLed1Input = Entry(master)
		self.BlueLed1Input.grid(row = 0, column = 2, padx = 20)
		self.RedLed1Input = Entry(master)
		self.RedLed1Input.grid(row = 1, column = 2, padx = 20)

		self.BlueLed2Input = Entry(master)
		self.BlueLed2Input.grid(row = 2, column = 2, padx = 20)
		self.RedLed2Input = Entry(master)
		self.RedLed2Input.grid(row = 3, column = 2, padx = 20)
		
		self.BlueLed3Input = Entry(master)
		self.BlueLed3Input.grid(row = 4, column = 2, padx = 20)
		self.RedLed3Input = Entry(master)
		self.RedLed3Input.grid(row = 5, column = 2, padx = 20)
		
		# ***** LED Enter Button ***** #
		
		self.BlueLed1Button = Button(master, text = "        Set Blue LED 1 (%)", command = self.BlueLed1Enter)
		self.BlueLed1Button.grid(row = 0, column = 3, sticky = E)
		self.RedLed1Button = Button(master, text = "         Set Red LED 1 (%)", command = self.RedLed1Enter)
		self.RedLed1Button.grid(row = 1, column = 3, sticky = E)

		self.BlueLed2Button = Button(master, text = "        Set Blue LED 2 (%)", command = self.BlueLed2Enter)
		self.BlueLed2Button.grid(row = 2, column = 3, sticky = E)
		self.RedLed2Button = Button(master, text = "         Set Red LED 2 (%)", command = self.RedLed2Enter)
		self.RedLed2Button.grid(row = 3, column = 3, sticky = E)
		
		self.BlueLed3 = Button(master, text = "        Set Blue LED 3 (%)", command = self.BlueLed3Enter)
		self.BlueLed3.grid(row = 4, column = 3, sticky = E)
		self.RedLed3 = Button(master, text = "         Set Red LED 3 (%)", command = self.RedLed3Enter)
		self.RedLed3.grid(row = 5, column = 3, sticky = E)
		
		
		# ***** Break Label ***** #
		
		self.BreakLabel1 = Label(master, text = "+----------------------------------------------------------------------------------------------------------------------------------------------+")
		self.BreakLabel1.grid(row = 7, columnspan = 4)
		
		# ***** Temperature Boxes ***** #
		
		self.TempLabel = Label(master, text = "Temperature")
		self.TempLabel.grid(row = 9, column = 0, sticky = W)

		self.TempValue = Label(master, text = "23", bg = "white")
		self.TempValue.grid(row = 9, column = 1, sticky = W, padx = 20)
		
		self.TempInput = Entry(master)
		self.TempInput.grid(row = 9, column = 2, padx = 20)
		
		self.TempButton = Button(master, text = "Set Temperatre (Deg C)", command = self.TempEnter)
		self.TempButton.grid(row = 9, column = 3, sticky = E)
		
		
		### ******************   Methods   ****************** ###
		
	def BlueLed1Enter(self):
		print("Blue LED 1 Entered")
		
	def RedLed1Enter(self):
		print("Red LED 1 Entered")
	
	def BlueLed2Enter(self):
		print("Blue LED 2 Entered")
		
	def RedLed2Enter(self):
		print("Red LED 2 Entered")
		
	def BlueLed3Enter(self):
		print("Blue LED 3 Entered")
		
	def RedLed3Enter(self):
		print("Red LED 3 Entered")
		
	def TempEnter(self):
		print("Temperature Entered")	



window = Tk()

arbi = ArbiGUI(window)


window.mainloop()

