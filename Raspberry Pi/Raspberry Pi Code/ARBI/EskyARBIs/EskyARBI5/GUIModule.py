#!/usr/bin/env python

# Import headers/modules
from Tkinter import *

class GUIClass(object):
	
	def __init__(self, GUItitle):
		
		self.GUItitle = GUItitle
		
		self.blueLED1State = ""
		self.blueLED2State = ""
		self.blueLED3State = ""
		self.redLED1State = ""
		self.redLED2State = ""
		self.redLED3State = ""
		
		self.insideTempState = ""
		self.waterTempState = ""
		
		self.ledOnTimeState = ""
		self.ledOffTimeState = ""
		self.flashStatusState = ""
	
	def getBlueLED1State(self):
		
		return self.blueLED1State

	def getBlueLED2State(self):
		
		return self.blueLED2State

	def getBlueLED3State(self):
		
		return self.blueLED3State

	def getRedLED1State(self):
		
		return self.redLED1State

	def getRedLED2State(self):
		
		return self.redLED2State

	def getRedLED3State(self):
		
		return self.redLED3State

	def getInsideTempState(self):
		
		return self.insideTempState

	def getWaterTempState(self):
		
		return self.waterTempState

	def getLedOnTimeState(self):
		
		return self.ledOnTimeState

	def getLedOffTimeState(self):
		
		return self.ledOffTimeState

	def getFlashStatusState(self):
		
		return self.flashStatusState
	
	def BlueLed1Set(self):
		
		self.blueLED1State = self.blueLed1Input.get()
		
	def BlueLed2Set(self):
		
		self.blueLED2State = self.blueLed2Input.get()
					
	def BlueLed3Set(self):
		
		self.blueLED3State = self.blueLed3Input.get()
			
	def RedLed1Set(self):
		
		self.redLED1State = self.redLed1Input.get()
			
	def RedLed2Set(self):
		
		self.redLED2State = self.redLed2Input.get()
			
	def RedLed3Set(self):
		
		self.redLED3State = self.redLed3Input.get()

	def InsideTempSet(self):
		
		self.insideTempState = self.insideTempInput.get()

	def WaterTempSet(self):
		
		self.waterTempState = self.waterTempInput.get()
		
	def LedOnTimeSet(self):
			
		if (self.flashStatusText.get() == "Flash"):

			self.ledOnTimeState = str(int(float(self.ledOnTimeInput.get()) * 1000))

		elif (self.flashStatusText.get() == "On"):
			
			self.ledOnTimeState = "On"
			
		else:
			
			self.ledOnTimeState = "Off"

	def LedOffTimeSet(self):

		if (self.flashStatusText.get() == "Flash"):

			self.ledOffTimeState = str(int(float(self.ledOffTimeInput.get()) * 1000))

		elif (self.flashStatusText.get() == "On"):
			
			self.ledOffTimeState = "On"
			
		else:
			
			self.ledOffTimeState = "Off"

	def FlashStatusToggle(self):
		
		if (self.flashStatusText.get() == ""):
			
			self.flashStatusText.set("Flash")
			
			self.ledOnTimeInput.delete(0, END)
			self.ledOnTimeInput.insert(END, "1")
				
			self.ledOffTimeInput.delete(0, END)
			self.ledOffTimeInput.insert(END, "1")

			self.LedOnTimeSet()
			self.LedOffTimeSet()
			
			self.flashStatusState = "Flash"
		
		elif (self.flashStatusText.get() == "Flash"):
				
			self.flashStatusText.set("On")
				
			self.ledOnTimeInput.delete(0, END)
			self.ledOnTimeInput.insert(END, "On")

			self.ledOffTimeInput.delete(0, END)
			self.ledOffTimeInput.insert(END, "On")
			
			self.LedOnTimeSet()
			self.LedOffTimeSet()
			
			self.flashStatusState = "On"			

		elif (self.flashStatusText.get() == "On"):
				
			self.flashStatusText.set("Off")
				
			self.ledOnTimeInput.delete(0, END)
			self.ledOnTimeInput.insert(END, "Off")

			self.ledOffTimeInput.delete(0, END)
			self.ledOffTimeInput.insert(END, "Off")
			
			self.LedOnTimeSet()
			self.LedOffTimeSet()
			
			self.flashStatusState = "Off"

		else:
				
			self.flashStatusText.set("Flash")
				
			self.ledOnTimeInput.delete(0, END)
			self.ledOnTimeInput.insert(END, "1")
				
			self.ledOffTimeInput.delete(0, END)
			self.ledOffTimeInput.insert(END, "1")

			self.LedOnTimeSet()
			self.LedOffTimeSet()
			
			self.flashStatusState = "Flash"

	def createGUI(self):
		
		root = Tk()
		
		### ***** Code for Resizing GUI ***** ###
				
		root.wm_title(self.GUItitle)		
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
		self.blueLed1Label = Label(frame, text = " Blue LED 1 Intensity (Lux):")
		self.blueLed1Label.grid(row = 1, column = 0, sticky = N+S+E+W)

		# Current value label (with variable text)
		self.blueLed1Text = StringVar()
		self.blueLed1Value = Label(frame, textvariable = self.blueLed1Text, bg = "white")
		self.blueLed1Value.grid(row = 1, column = 1, sticky = N+S+E+W, padx = 20)

		# Enter setpoint button
		self.blueLed1Button = Button(frame, text = "Set Blue LED 1 (PWM Ratio/65535):", command = self.BlueLed1Set)
		self.blueLed1Button.grid(row = 1, column = 2, sticky = N+S+E+W)

		# Setpoint input entry box (with default value inserted)
		self.blueLed1Input = Entry(frame)
		self.blueLed1Input.insert(END, "")
		self.blueLed1Input.grid(row = 1, column = 3, padx = 20)
		
		
		
		### ***** Blue LED 2 Widgets ***** ###

		# Parameter description label (with static text)
		self.blueLed2Label = Label(frame, text = " Blue LED 2 Intensity (Lux):")
		self.blueLed2Label.grid(row = 2, column = 0, sticky = N+S+E+W)

		# Current value label (with variable text)
		self.blueLed2Text = StringVar()
		self.blueLed2Value = Label(frame, textvariable = self.blueLed2Text, bg = "white")
		self.blueLed2Value.grid(row = 2, column = 1, sticky = N+S+E+W, padx = 20)

		# Enter setpoint button
		self.blueLed2Button = Button(frame, text = "Set Blue LED 2 (PWM Ratio/65535):", command = self.BlueLed2Set)
		self.blueLed2Button.grid(row = 2, column = 2, sticky = N+S+E+W)

		# Setpoint input entry box (with default value inserted) 
		self.blueLed2Input = Entry(frame)
		self.blueLed2Input.insert(END, "")
		self.blueLed2Input.grid(row = 2, column = 3, padx = 20)



		### ***** Blue LED 3 Widgets ***** ###

		# Parameter description label (with static text)
		self.blueLed3Label = Label(frame, text = " Blue LED 3 Intensity (Lux):")
		self.blueLed3Label.grid(row = 3, column = 0, sticky = N+S+E+W)

		# Current value label (with variable text)
		self.blueLed3Text = StringVar()
		self.blueLed3Value = Label(frame, textvariable = self.blueLed3Text, bg = "white")
		self.blueLed3Value.grid(row = 3, column = 1, sticky = N+S+E+W, padx = 20)

		# Enter setpoint button
		self.blueLed3Button = Button(frame, text = "Set Blue LED 3 (PWM Ratio/65535):", command = self.BlueLed3Set)
		self.blueLed3Button.grid(row = 3, column = 2, sticky = N+S+E+W)

		# Setpoint input entry box (with default value inserted) 
		self.blueLed3Input = Entry(frame)
		self.blueLed3Input.insert(END, "")
		self.blueLed3Input.grid(row = 3, column = 3, padx = 20)



		### ***** Red LED 1 Widgets ***** ###

		# Parameter description label (with static text)
		self.redLed1Label = Label(frame, text = "Red LED 1 Intensity (Lux):")
		self.redLed1Label.grid(row = 4, column = 0, sticky = N+S+E+W)

		# Current value label (with variable text)
		self.redLed1Text = StringVar()
		self.redLed1Value = Label(frame, textvariable = self.redLed1Text, bg = "white")
		self.redLed1Value.grid(row = 4, column = 1, sticky = N+S+E+W, padx = 20)

		# Enter setpoint button
		self.redLed1Button = Button(frame, text = "Set Red LED 1 (PWM Ratio/65535):", command = self.RedLed1Set)
		self.redLed1Button.grid(row = 4, column = 2, sticky = N+S+E+W)

		# Setpoint input entry box (with default value inserted) 
		self.redLed1Input = Entry(frame)
		self.redLed1Input.insert(END, "")
		self.redLed1Input.grid(row = 4, column = 3, padx = 20)



		### ***** Red LED 2 Widgets ***** ###

		# Parameter description label (with static text)
		self.redLed2Label = Label(frame, text = "Red LED 2 Intensity (Lux):")
		self.redLed2Label.grid(row = 5, column = 0, sticky = N+S+E+W)

		# Current value label (with variable text)
		self.redLed2Text = StringVar()
		self.redLed2Value = Label(frame, textvariable = self.redLed2Text, bg = "white")
		self.redLed2Value.grid(row = 5, column = 1, sticky = N+S+E+W, padx = 20)

		# Enter setpoint button
		self.redLed2Button = Button(frame, text = "Set Red LED 2 (PWM Ratio/65535):", command = self.RedLed2Set)
		self.redLed2Button.grid(row = 5, column = 2, sticky = N+S+E+W)

		# Setpoint input entry box (with default value inserted) 
		self.redLed2Input = Entry(frame)
		self.redLed2Input.insert(END, "")
		self.redLed2Input.grid(row = 5, column = 3, padx = 20)



		### ***** Red LED 3 Widgets ***** ###

		# Parameter description label (with static text)
		self.redLed3Label = Label(frame, text = "Red LED 3 Intensity (Lux):")
		self.redLed3Label.grid(row = 6, column = 0, sticky = N+S+E+W)

		# Current value label (with variable text)
		self.redLed3Text = StringVar()
		self.redLed3Value = Label(frame, textvariable = self.redLed3Text, bg = "white")
		self.redLed3Value.grid(row = 6, column = 1, sticky = N+S+E+W, padx = 20)

		# Enter setpoint button
		self.redLed3Button = Button(frame, text = "Set Red LED 3 (PWM Ratio/65535):", command = self.RedLed3Set)
		self.redLed3Button.grid(row = 6, column = 2, sticky = N+S+E+W)

		# Setpoint input entry box (with default value inserted) 
		self.redLed3Input = Entry(frame)
		self.redLed3Input.insert(END, "")
		self.redLed3Input.grid(row = 6, column = 3, padx = 20)



		### ***** Break Label 1 ***** ###
				
		breakLabel = ""
				
		while len(breakLabel) < 250:
			breakLabel += "-"
				
		self.breakLabel1 = Label(frame, text = breakLabel)
		self.breakLabel1.grid(row = 7, columnspan = 4)
				
				
				
		### ***** Inside Temperature 1 Widgets ***** ###

		# Parameter description label (with static text)
		self.insideTemp1Label = Label(frame, text = "Inside Temperature 1 (deg C):")
		self.insideTemp1Label.grid(row = 8, column = 0, sticky = N+S+E+W)

		# Current value label (with variable text)
		self.insideTemp1Text = StringVar()
		self.insideTemp1Value = Label(frame, textvariable = self.insideTemp1Text, bg = "white")
		self.insideTemp1Value.grid(row = 8, column = 1, sticky = N+S+E+W, padx = 20)



		### ***** Inside Temperature 2 Widgets ***** ###

		# Parameter description label (with static text)
		self.insideTemp2Label = Label(frame, text = "Inside Temperature 2 (deg C):")
		self.insideTemp2Label.grid(row = 9, column = 0, sticky = N+S+E+W)

		# Current value label (with variable text)
		self.insideTemp2Text = StringVar()
		self.insideTemp2Value = Label(frame, textvariable = self.insideTemp2Text, bg = "white")
		self.insideTemp2Value.grid(row = 9, column = 1, sticky = N+S+E+W, padx = 20)



		### ***** Inside Temperature 3 Widgets ***** ###

		# Parameter description label (with static text)
		self.insideTemp3Label = Label(frame, text = "Inside Temperature 3 (deg C):")
		self.insideTemp3Label.grid(row = 10, column = 0, sticky = N+S+E+W)

		# Current value label (with variable text)
		self.insideTemp3Text = StringVar()
		self.insideTemp3Value = Label(frame, textvariable = self.insideTemp3Text, bg = "white")
		self.insideTemp3Value.grid(row = 10, column = 1, sticky = N+S+E+W, padx = 20)



		### ***** Inside Temperature 4 Widgets ***** ###

		# Parameter description label (with static text)
		self.insideTemp4Label = Label(frame, text = "Inside Temperature 4 (deg C):")
		self.insideTemp4Label.grid(row = 11, column = 0, sticky = N+S+E+W)

		# Current value label (with variable text)
		self.insideTemp4Text = StringVar()
		self.insideTemp4Value = Label(frame, textvariable = self.insideTemp4Text, bg = "white")
		self.insideTemp4Value.grid(row = 11, column = 1, sticky = N+S+E+W, padx = 20)



		### ***** Inside Temperature 5 Widgets ***** ###

		# Parameter description label (with static text)
		self.insideTemp5Label = Label(frame, text = "Inside Temperature 5 (deg C):")
		self.insideTemp5Label.grid(row = 12, column = 0, sticky = N+S+E+W)

		# Current value label (with variable text)
		self.insideTemp5Text = StringVar()
		self.insideTemp5Value = Label(frame, textvariable = self.insideTemp5Text, bg = "white")
		self.insideTemp5Value.grid(row = 12, column = 1, sticky = N+S+E+W, padx = 20)



		### ***** Inside Temperature 6 Widgets ***** ###

		# Parameter description label (with static text)
		self.insideTemp6Label = Label(frame, text = "Inside Temperature 6 (deg C):")
		self.insideTemp6Label.grid(row = 13, column = 0, sticky = N+S+E+W)

		# Current value label (with variable text)
		self.insideTemp6Text = StringVar()
		self.insideTemp6Value = Label(frame, textvariable = self.insideTemp6Text, bg = "white")
		self.insideTemp6Value.grid(row = 13, column = 1, sticky = N+S+E+W, padx = 20)


				
		### ***** Water Temperature 1 Widgets ***** ###

		# Paramter description label (with static text)
		self.waterTemp1Label = Label(frame, text = "Water Temperature 1 (deg C):")
		self.waterTemp1Label.grid(row = 14, column = 0, sticky = N+S+E+W)

		# Current value label (with variable text)
		self.waterTemp1Text = StringVar()
		self.waterTemp1Value = Label(frame, textvariable = self.waterTemp1Text, bg = "white")
		self.waterTemp1Value.grid(row = 14, column = 1, sticky = N+S+E+W, padx = 20)



		### ***** Water Temperature 2 Widgets ***** ###

		# Paramter description label (with static text)
		self.waterTemp2Label = Label(frame, text = "Water Temperature 2 (deg C):")
		self.waterTemp2Label.grid(row = 15, column = 0, sticky = N+S+E+W)

		# Current value label (with variable text)
		self.waterTemp2Text = StringVar()
		self.waterTemp2Value = Label(frame, textvariable = self.waterTemp2Text, bg = "white")
		self.waterTemp2Value.grid(row = 15, column = 1, sticky = N+S+E+W, padx = 20)
				
				

		### ***** Inside Temperature All Setpoint Widgets ***** ###

		# Enter setpoint button
		self.insideTempButton = Button(frame, text = "Set Inside Temperatre (deg C):", command = self.InsideTempSet)
		self.insideTempButton.grid(row = 10, column = 2, sticky = N+S+E+W)

		# Setpoint input entry box (with default value inserted) 
		self.insideTempInput = Entry(frame)
		self.insideTempInput.insert(END, "")
		self.insideTempInput.grid(row = 10, column = 3, padx = 20)



		### ***** Water Temperature All Setpoint Widgets ***** ###

		# Enter setpoint button
		self.waterTempButton = Button(frame, text = "Set Water Temperatre (deg C):", command = self.WaterTempSet)
		self.waterTempButton.grid(row = 13, column = 2, sticky = N+S+E+W)

		# Setpoint input entry box (with default value inserted) 
		self.waterTempInput = Entry(frame)
		self.waterTempInput.insert(END, "")
		self.waterTempInput.grid(row = 13, column = 3, padx = 20)
				
					
					
		### ***** Break Label 2 ***** ###
				
		self.breakLabel2 = Label(frame, text = breakLabel)
		self.breakLabel2.grid(row = 16, columnspan = 4)


				
		### ***** Flow Meter Widgets ***** ###

		# Paramter description label (with static text)	
		self.flowMeterTitle = Label(frame, text = "Flow Meter (L/min):")
		self.flowMeterTitle.grid(row = 18, column = 0, sticky = N+S+E+W)

		# Current value label (with variable text)
		self.flowMeterText = StringVar()
		self.flowMeterLabel = Label(frame, textvariable = self.flowMeterText, bg = "white")
		self.flowMeterLabel.grid(row = 18, column = 1, sticky = N+S+E+W, padx = 20)		
				
				
				
		### ***** LED on time Widgets ***** ###

		# Enter setpoint button		
		self.ledOnTimeButton = Button(frame, text = "Set LED on time (sec):", command = self.LedOnTimeSet)
		self.ledOnTimeButton.grid(row = 17, column = 2, sticky = N+S+E+W)

		# Setpoint input entry box 		
		self.ledOnTimeInput = Entry(frame)
		self.ledOnTimeInput.insert(END, "")
		self.ledOnTimeInput.grid(row = 17, column = 3, padx = 20)
				
				
				
		### ***** LED off time Widgets ***** ###

		# Enter setpoint button
		self.ledOffTimeButton = Button(frame, text = "Set LED off time (sec):", command = self.LedOffTimeSet)
		self.ledOffTimeButton.grid(row = 18, column = 2, sticky = N+S+E+W)

		# Setpoint input entry box				
		self.ledOffTimeInput = Entry(frame)
		self.ledOffTimeInput.insert(END, "")
		self.ledOffTimeInput.grid(row = 18, column = 3, padx = 20)
				

				
		### ***** LED permanent settings on/off/flash Widgets ***** ###

		# Enter led mode button
		self.flashStatusButton = Button(frame, text = "LED mode:", command = self.FlashStatusToggle)
		self.flashStatusButton.grid(row = 19, column = 2, sticky = N+S+E+W)	

		# Current led mode label (variable text with default text set)
		self.flashStatusText = StringVar()
		self.flashStatusText.set("")		
		self.flashStatusValue = Label(frame, textvariable = self.flashStatusText, bg = "white")
		self.flashStatusValue.grid(row = 19, column = 3, sticky = N+S+E+W, padx = 20)


				
		### ***** Break Label 3 ***** ###
				
		self.breakLabel2 = Label(frame, text = breakLabel)
		self.breakLabel2.grid(row = 20, columnspan = 4)


				
		### ***** Update Current Values Button ***** ###
				
		self.updateCurValButton = Button(frame, text = "Update Current Values")
		self.updateCurValButton.grid(row = 21, column = 0, columnspan = 4, sticky = N+S+E+W)
		
		
		### ***** Rescale GUI size ***** ###
		
		for x in range(4):
			Grid.columnconfigure(frame, x, weight = 1)

		for y in range(22):
			Grid.rowconfigure(frame, y, weight = 1)
			
		root.mainloop()