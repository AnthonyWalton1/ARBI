#!/usr/bin/env python

##### *************** Initialisation Code *************** #####


# Import required libraries and setup serial com port with Arduino
from Tkinter import *
import serial
ser = serial.Serial('/dev/ttyACM0', 9600)
import time

# Start a new GUI																												
root = Tk()





##### *************** Function Definitions *************** #####


# Function called for setting blue LED 1 luminosity
def BlueLed1Set():
		
	input = blueLed1Input.get()
		
	while (len(input) < 3):
		input = "0" + input
			
	print("01_" + input + "\r\n")
	ser.write("01_" + input + "\r\n")	



# Function called for setting blue LED 2 luminosity
def BlueLed2Set():

	input = blueLed2Input.get()
		
	while (len(input) < 3):
		input = "0" + input
			
	print("02_" + input + "\r\n")
	ser.write("02_" + input + "\r\n")	
			


# Function called for setting blue LED 3 luminosity
def BlueLed3Set():

	input = blueLed3Input.get()
		
	while (len(input) < 3):
		input = "0" + input
			
	print("03_" + input + "\r\n")
	ser.write("03_" + input + "\r\n")							
			


# Function called for setting red LED 1 luminosity		
def RedLed1Set():
		
	input = redLed1Input.get()
		
	while (len(input) < 3):
		input = "0" + input
			
	print("04_" + input + "\r\n")
	ser.write("04_" + input + "\r\n")	
					


# Function called for setting red LED 2 luminosity	
def RedLed2Set():

	input = redLed2Input.get()
		
	while (len(input) < 3):
		input = "0" + input
			
	print("05_" + input + "\r\n")
	ser.write("05_" + input + "\r\n")	
			


# Function called for setting red LED 3 luminosity		
def RedLed3Set():
		
	input = redLed3Input.get()
		
	while (len(input) < 3):
		input = "0" + input
			
	print("06_" + input + "\r\n")
	ser.write("06_" + input + "\r\n")	

			

# Function called for setting inside air temperature	
def InsideTempSet():

	input = insideTempInput.get()
		
	while (len(input) < 3):
		input = "0" + input
			
	print("07_" + input + "\r\n")
	ser.write("07_" + input + "\r\n")	
			
	

# Function called for setting water temperature	
def WaterTempSet():

	input = waterTempInput.get()
		
	while (len(input) < 3):
		input = "0" + input
			
	print("08_" + input + "\r\n")
	ser.write("08_" + input + "\r\n")	
			


# Function called for setting LED on time			
def LedOnTimeSet():
		
	if (flashStatusText.get() == "Flash"):
			
		input = str(int(float(ledOnTimeInput.get()) * 1000))
		
		while (len(input) < 9):
			input = "0" + input
		
		print("09_" + input + "\r\n")
		ser.write("09_" + input + "\r\n")
		
	elif (flashStatusText.get() == "On"):
			
		print("09_100000000\r\n")
		ser.write("09_100000000\r\n")
			
	elif (flashStatusText.get() == "Off"):
			
		print("09_200000000\r\n")
		ser.write("09_200000000\r\n")
		


# Function called for setting LED off time
def LedOffTimeSet():

	if (flashStatusText.get() == "Flash"):
			
		input = str(int(float(ledOffTimeInput.get()) * 1000))
		
		while (len(input) < 9):
			input = "0" + input
		
		print("10_" + input + "\r\n")
		ser.write("10_" + input + "\r\n")
		
	elif (flashStatusText.get() == "On"):
			
		print("10_100000000\r\n")
		ser.write("10_100000000\r\n")
		
	elif (flashStatusText.get() == "Off"):
			
		print("10_200000000\r\n")
		ser.write("10_200000000\r\n")
	


# Function called for changing LED frequency state entry in Entry Box widget	
def FlashStatusToggle():
		
	if (flashStatusText.get() == "Flash"):
			
		flashStatusText.set("On")
			
		ledOnTimeInput.delete(0, END)
		ledOnTimeInput.insert(END, "On")

		ledOffTimeInput.delete(0, END)
		ledOffTimeInput.insert(END, "On")
			
	elif (flashStatusText.get() == "On"):
			
		flashStatusText.set("Off")
			
		ledOnTimeInput.delete(0, END)
		ledOnTimeInput.insert(END, "Off")
			
		ledOffTimeInput.delete(0, END)
		ledOffTimeInput.insert(END, "Off")
			
	else:
			
		flashStatusText.set("Flash")
			
		ledOnTimeInput.delete(0, END)
		ledOnTimeInput.insert(END, "1")
			
		ledOffTimeInput.delete(0, END)
		ledOffTimeInput.insert(END, "1")
		

			
# Function called for writing to the text file every X number of seconds. Also updates the current values on GUI screen
def WriteToTextFile():
	
	# Open the text file each time since we close it each time
	# Note: "a" means opening the text file in append mode. 
	# Note: This is required as "w" writing mode overwrites the previous file once it is closed an re-opened.
	# Note: we want to add the next set of data to the pre-existing list, which is what append mode does.
	text_file = open("arbi7_text.txt", "a")
	
	# Send the signal to the Arduino to send the Raspberry Pi all data
	ser.write("99_000\r\n")
		
	# Wait for the data to be received from the Arduino
	time.sleep(1)
	
	# Call this function to run again in 4 seconds (total time interval is thus 1 second wait + 4 second iterative timer = data every 5 seconds)
	# Note: this is a self-iterating function process
	root.after(60000, WriteToTextFile)
	
	# Read the first byte and initialise the input string
	val = ser.read(1)
	line = ""
	
	# While the enter signifying the end of the transmission string has not been encountered
	while val not in ["\n"]:
		
		# If it is not the carraige return immeadiately before the new line (in the enter)
		if val != "\r":
			line += val
		
		# Read the next byte/character	
		val = ser.read(1)
	
	# Read the next 2 bytes to clear out the enter key
	val = ser.read(2)
	
	# Print the input string for verification			
	print("\r\n\r\n" + line)
	
	# Split the input string at the spaces to separate data
	values = line.split(" ")
	
	# Include error checking that checks that the indexed element will actually exist based on splits at " " and "_"
	# Note: the final enter \r\n isn't included in calculating len(line)
		
	# Reset error flags to off
	error = 0
	rtcError = 0
	
	if len(line) == 152:
		print("correct length")
			
		if line[2] == "_":
			print("01 correct")
			blueLed1Text.set(values[0].split("_")[1])
		else:
			print("Return string: wrong format 01")
			error = 1
			
		if line[9] == "_" and line[6] == " ":
			print("02 correct")
			blueLed2Text.set(values[1].split("_")[1])
		else:
			print("Return string: wrong format 02")
			error = 1
			
		if line[16] == "_" and line[13] == " ":
			print("03 correct")
			blueLed3Text.set(values[2].split("_")[1])
		else:
			print("Return string: wrong format 03")
			error = 1
		
		if line[23] == "_" and line[20] == " ":
			print("04 correct")
			redLed1Text.set(values[3].split("_")[1])
		else:
			print("Return string: wrong format 04")
			error = 1
		
		if line[30] == "_" and line[27] == " ":
			print("05 correct")
			redLed2Text.set(values[4].split("_")[1])
		else:
			print("Return string: wrong format 05")
			error = 1
		
		if line[37] == "_" and line[34] == " ":
			print("06 correct")
			redLed3Text.set(values[5].split("_")[1])
		else:
			print("Return string: wrong format 06")
			error = 1		
		
		if line[44] == "_" and line[41] == " ":
			print("07 correct")
			insideTempText.set(values[6].split("_")[1])
		else:
			print("Return string: wrong format 07")
			error = 1
					
		if line[51] == "_" and line[48] == " ":
			print("08 correct")
			waterTempText.set(values[7].split("_")[1])
		else:
			print("Return string: wrong format 08")
			error = 1
		
		if line[58] == "_" and line[55] == " ":\
			print("09 correct")
		else:
			print("Return string: wrong format 09")
			error = 1
	
		if line[71] == "_" and line[68] == " ":
			print("10 correct")
		else:
			print("Return string: wrong format 10")
			error = 1
	
		if line[84] == "_" and line[81] == " ":
			print("11 correct")
			flowMeter.set(str(float(values[10].split("_")[1])/10))
		else:
			print("Return string: wrong format 11")
			error = 1
		
		if line[91] == "_" and line[88] == " ":
			print("12 correct")
			averageTemp1.set(values[11].split("_")[1])
			
			# Extract value for Data Logging
			airAvTemp = values[11].split("_")[1]
		
		else:
			print("Return string: wrong format 12")
			error = 1
			rtcError = 1
			
		if line[98] == "_" and line[95] == " ":
			print("13 correct")
			averageTemp2.set(values[12].split("_")[1])
		else:
			print("Return string: wrong format 13")
			error = 1
			
		if line[105] == "_" and line[102] == " ":
			print("14 correct")
		else:
			print("Return string: wrong format 14")
			error = 1
			
		if line[112] == "_" and line[109] == " ":
			print("15 correct")
			seconds = values[14].split("_")[1]
		else:
			print("Return string: wrong format 15")
			error = 1
			rtcError = 1
			
		if line[119] == "_" and line[116] == " ":
			print("16 correct")
			minutes = values[15].split("_")[1]
		else:
			print("Return string: wrong format 16")
			error = 1
			rtcError = 1
			
		if line[126] == "_" and line[123] == " ":
			print("17 correct")
			hours = values[16].split("_")[1]
		else:
			print("Return string: wrong format 17")
			error = 1
			rtcError = 1
			
		if line[133] == "_" and line[130] == " ":
			print("18 correct")
			days = values[17].split("_")[1]
		else:
			print("Return string: wrong format 18")
			error = 1
			rtcError = 1
			
		if line[140] == "_" and line[137] == " ":
			print("19 correct")
			months = values[18].split("_")[1]
		else:
			print("Return string: wrong format 19")
			error = 1
			rtcError = 1
			
		if line[147] == "_" and line[144] == " ":
			print("20 correct")
			years = values[19].split("_")[1]
		else:
			print("Return string: wrong format 20")
			error = 1
			rtcError = 1
				
	else:
		print("Return string: wrong length")
		error = 1	
	
	# If any errors occured print an error flag
	if error == 1:
		print("Error Flag")
			
	# Only run RTC component code if not error occured with data logging data
		
	if rtcError == 0:
		# Convert all external RTC component (Real-Time Clock) time values to seconds
		secondsData = str(int(seconds) + int(minutes)*60 + int(hours)*60*60 + int(days)*60*60*24)
	
		# Concatentate the string in comma separated format for Excel
		# Note: enter means a new row in Excel (no choice)
		# Note: comma means a new column in Excel (choice, could also be a tab, etc)
		# Note: data structure wrt columns is (time, value) for Excel graphing
		msg = secondsData + "," + airAvTemp + "\r\n"
	
		# Print the message for verification
		print(msg)
	
		# Write the data with the correct format into the file
		text_file.write(msg)
	
		# Close the file each time so that the writing is saved
		text_file.close()
	else:
		print("rtcError Flag")




	
##### ************** GUI Initialisation Code *************** #####


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



### ***** Blue LED 2 Widgets ***** ###

# Parameter description label (with static text)
blueLed2Label = Label(frame, text = " Blue LED 2 Intensity (Lux):")
blueLed2Label.grid(row = 2, column = 0, sticky = N+S+E+W)

# Current value label (with variable text)
blueLed2Text = StringVar()
blueLed2Value = Label(frame, textvariable = blueLed2Text, bg = "white")
blueLed2Value.grid(row = 2, column = 1, sticky = N+S+E+W, padx = 20)

# Enter setpoint button
blueLed2Button = Button(frame, text = "Set Blue LED 2 (PWM Ratio/65535):", command = BlueLed2Set)
blueLed2Button.grid(row = 2, column = 2, sticky = N+S+E+W)

# Setpoint input entry box (with default value inserted) 
blueLed2Input = Entry(frame)
blueLed2Input.insert(END, "128")
blueLed2Input.grid(row = 2, column = 3, padx = 20)



### ***** Blue LED 3 Widgets ***** ###

# Parameter description label (with static text)
blueLed3Label = Label(frame, text = " Blue LED 3 Intensity (Lux):")
blueLed3Label.grid(row = 3, column = 0, sticky = N+S+E+W)

# Current value label (with variable text)
blueLed3Text = StringVar()
blueLed3Value = Label(frame, textvariable = blueLed3Text, bg = "white")
blueLed3Value.grid(row = 3, column = 1, sticky = N+S+E+W, padx = 20)

# Enter setpoint button
blueLed3Button = Button(frame, text = "Set Blue LED 3 (PWM Ratio/65535):", command = BlueLed3Set)
blueLed3Button.grid(row = 3, column = 2, sticky = N+S+E+W)

# Setpoint input entry box (with default value inserted) 
blueLed3Input = Entry(frame)
blueLed3Input.insert(END, "128")
blueLed3Input.grid(row = 3, column = 3, padx = 20)



### ***** Red LED 1 Widgets ***** ###

# Parameter description label (with static text)
redLed1Label = Label(frame, text = "Red LED 1 Intensity (Lux):")
redLed1Label.grid(row = 4, column = 0, sticky = N+S+E+W)


# Current value label (with variable text)
redLed1Text = StringVar()
redLed1Value = Label(frame, textvariable = redLed1Text, bg = "white")
redLed1Value.grid(row = 4, column = 1, sticky = N+S+E+W, padx = 20)

# Enter setpoint button
redLed1Button = Button(frame, text = "Set Red LED 1 (PWM Ratio/65535):", command = RedLed1Set)
redLed1Button.grid(row = 4, column = 2, sticky = N+S+E+W)

# Setpoint input entry box (with default value inserted) 
redLed1Input = Entry(frame)
redLed1Input.insert(END, "128")
redLed1Input.grid(row = 4, column = 3, padx = 20)


### ***** Red LED 2 Widgets ***** ###

# Parameter description label (with static text)
redLed2Label = Label(frame, text = "Red LED 2 Intensity (Lux):")
redLed2Label.grid(row = 5, column = 0, sticky = N+S+E+W)

# Current value label (with variable text)
redLed2Text = StringVar()
redLed2Value = Label(frame, textvariable = redLed2Text, bg = "white")
redLed2Value.grid(row = 5, column = 1, sticky = N+S+E+W, padx = 20)

# Enter setpoint button
redLed2Button = Button(frame, text = "Set Red LED 2 (PWM Ratio/65535):", command = RedLed2Set)
redLed2Button.grid(row = 5, column = 2, sticky = N+S+E+W)

# Setpoint input entry box (with default value inserted) 
redLed2Input = Entry(frame)
redLed2Input.insert(END, "128")
redLed2Input.grid(row = 5, column = 3, padx = 20)


### ***** Red LED 3 Widgets ***** ###

# Parameter description label (with static text)
redLed3Label = Label(frame, text = "Red LED 3 Intensity (Lux):")
redLed3Label.grid(row = 6, column = 0, sticky = N+S+E+W)

# Current value label (with variable text)
redLed3Text = StringVar()
redLed3Value = Label(frame, textvariable = redLed3Text, bg = "white")
redLed3Value.grid(row = 6, column = 1, sticky = N+S+E+W, padx = 20)

# Enter setpoint button
redLed3Button = Button(frame, text = "Set Red LED 3 (PWM Ratio/65535):", command = RedLed3Set)
redLed3Button.grid(row = 6, column = 2, sticky = N+S+E+W)

# Setpoint input entry box (with default value inserted) 
redLed3Input = Entry(frame)
redLed3Input.insert(END, "128")
redLed3Input.grid(row = 6, column = 3, padx = 20)



### ***** Break Label 1 ***** ###
		
breakLabel = ""
		
while len(breakLabel) < 250:
	breakLabel += "-"
		
breakLabel1 = Label(frame, text = breakLabel)
breakLabel1.grid(row = 7, columnspan = 4)
		
		
		
### ***** Inside Temperature 1 Widgets ***** ###

# Parameter description label (with static text)
insideTemp1Label = Label(frame, text = "Inside Temperature 1 (deg C):")
insideTemp1Label.grid(row = 8, column = 0, sticky = N+S+E+W)

# Current value label (with variable text)
insideTemp1Text = StringVar()
insideTemp1Value = Label(frame, textvariable = insideTemp1Text, bg = "white")
insideTemp1Value.grid(row = 8, column = 1, sticky = N+S+E+W, padx = 20)



### ***** Inside Temperature 2 Widgets ***** ###

# Parameter description label (with static text)
insideTemp2Label = Label(frame, text = "Inside Temperature 2 (deg C):")
insideTemp2Label.grid(row = 9, column = 0, sticky = N+S+E+W)

# Current value label (with variable text)
insideTemp2Text = StringVar()
insideTemp2Value = Label(frame, textvariable = insideTemp2Text, bg = "white")
insideTemp2Value.grid(row = 9, column = 1, sticky = N+S+E+W, padx = 20)



### ***** Inside Temperature 3 Widgets ***** ###

# Parameter description label (with static text)
insideTemp3Label = Label(frame, text = "Inside Temperature 3 (deg C):")
insideTemp3Label.grid(row = 10, column = 0, sticky = N+S+E+W)

# Current value label (with variable text)
insideTemp3Text = StringVar()
insideTemp3Value = Label(frame, textvariable = insideTemp3Text, bg = "white")
insideTemp3Value.grid(row = 10, column = 1, sticky = N+S+E+W, padx = 20)



### ***** Inside Temperature 4 Widgets ***** ###

# Parameter description label (with static text)
insideTemp4Label = Label(frame, text = "Inside Temperature 4 (deg C):")
insideTemp4Label.grid(row = 11, column = 0, sticky = N+S+E+W)

# Current value label (with variable text)
insideTemp4Text = StringVar()
insideTemp4Value = Label(frame, textvariable = insideTemp4Text, bg = "white")
insideTemp4Value.grid(row = 11, column = 1, sticky = N+S+E+W, padx = 20)



### ***** Inside Temperature 5 Widgets ***** ###

# Parameter description label (with static text)
insideTemp5Label = Label(frame, text = "Inside Temperature 5 (deg C):")
insideTemp5Label.grid(row = 12, column = 0, sticky = N+S+E+W)

# Current value label (with variable text)
insideTemp5Text = StringVar()
insideTemp5Value = Label(frame, textvariable = insideTemp5Text, bg = "white")
insideTemp5Value.grid(row = 12, column = 1, sticky = N+S+E+W, padx = 20)



### ***** Inside Temperature 6 Widgets ***** ###

# Parameter description label (with static text)
insideTemp6Label = Label(frame, text = "Inside Temperature 6 (deg C):")
insideTemp6Label.grid(row = 13, column = 0, sticky = N+S+E+W)

# Current value label (with variable text)
insideTemp6Text = StringVar()
insideTemp6Value = Label(frame, textvariable = insideTemp6Text, bg = "white")
insideTemp6Value.grid(row = 13, column = 1, sticky = N+S+E+W, padx = 20)


		
### ***** Water Temperature 1 Widgets ***** ###

# Paramter description label (with static text)
waterTemp1Label = Label(frame, text = "Water Temperature 1 (deg C):")
waterTemp1Label.grid(row = 14, column = 0, sticky = N+S+E+W)

# Current value label (with variable text)
waterTemp1Text = StringVar()
waterTemp1Value = Label(frame, textvariable = waterTemp1Text, bg = "white")
waterTemp1Value.grid(row = 14, column = 1, sticky = N+S+E+W, padx = 20)



### ***** Water Temperature 2 Widgets ***** ###

# Paramter description label (with static text)
waterTemp2Label = Label(frame, text = "Water Temperature 2 (deg C):")
waterTemp2Label.grid(row = 15, column = 0, sticky = N+S+E+W)

# Current value label (with variable text)
waterTemp2Text = StringVar()
waterTemp2Value = Label(frame, textvariable = waterTemp2Text, bg = "white")
waterTemp2Value.grid(row = 15, column = 1, sticky = N+S+E+W, padx = 20)
		
		

### ***** Inside Temperature All Setpoint Widgets ***** ###

# Enter setpoint button
insideTempButton = Button(frame, text = "Set Inside Temperatre (deg C):", command = InsideTempSet)
insideTempButton.grid(row = 10, column = 2, sticky = N+S+E+W)

# Setpoint input entry box (with default value inserted) 
insideTempInput = Entry(frame)
insideTempInput.insert(END, "23")
insideTempInput.grid(row = 10, column = 3, padx = 20)



### ***** Water Temperature All Setpoint Widgets ***** ###

# Enter setpoint button
waterTempButton = Button(frame, text = "Set Water Temperatre (deg C):", command = WaterTempSet)
waterTempButton.grid(row = 13, column = 2, sticky = N+S+E+W)

# Setpoint input entry box (with default value inserted) 
waterTempInput = Entry(frame)
waterTempInput.insert(END, "10")
waterTempInput.grid(row = 13, column = 3, padx = 20)
		
			
			
### ***** Break Label 2 ***** ###
		
breakLabel2 = Label(frame, text = breakLabel)
breakLabel2.grid(row = 16, columnspan = 4)


		
### ***** Flow Meter Widgets ***** ###

# Paramter description label (with static text)	
flowMeterTitle = Label(frame, text = "Flow Meter (L/min):")
flowMeterTitle.grid(row = 18, column = 0, sticky = N+S+E+W)

# Current value label (with variable text)
flowMeter = StringVar()
flowMeterLabel = Label(frame, textvariable = flowMeter, bg = "white")
flowMeterLabel.grid(row = 18, column = 1, sticky = N+S+E+W, padx = 20)		
		
		
		
### ***** LED on time Widgets ***** ###

# Enter setpoint button		
ledOnTimeButton = Button(frame, text = "Set LED on time (sec):", command = LedOnTimeSet)
ledOnTimeButton.grid(row = 17, column = 2, sticky = N+S+E+W)

# Setpoint input entry box 		
ledOnTimeInput = Entry(frame)
ledOnTimeInput.insert(END, "1")
ledOnTimeInput.grid(row = 17, column = 3, padx = 20)
		
		
		
### ***** LED off time Widgets ***** ###

# Enter setpoint button
ledOffTimeButton = Button(frame, text = "Set LED off time (sec):", command = LedOffTimeSet)
ledOffTimeButton.grid(row = 18, column = 2, sticky = N+S+E+W)

# Setpoint input entry box				
ledOffTimeInput = Entry(frame)
ledOffTimeInput.insert(END, "1")
ledOffTimeInput.grid(row = 18, column = 3, padx = 20)
		

		
### ***** LED permanent settings on/off/flash Widgets ***** ###

# Enter led mode button
flashStatusButton = Button(frame, text = "LED mode:", command = FlashStatusToggle)
flashStatusButton.grid(row = 19, column = 2, sticky = N+S+E+W)	

# Current led mode label (variable text with default text set)
flashStatusText = StringVar()
flashStatusText.set("Flash")		
flashStatusValue = Label(frame, textvariable = flashStatusText, bg = "white")
flashStatusValue.grid(row = 19, column = 3, sticky = N+S+E+W, padx = 20)


		
### ***** Break Label 3 ***** ###
		
breakLabel2 = Label(frame, text = breakLabel)
breakLabel2.grid(row = 20, columnspan = 4)


		
### ***** Update Current Values Button ***** ###
		
updateCurValButton = Button(frame, text = "Update Current Values")
updateCurValButton.grid(row = 21, column = 0, columnspan = 4, sticky = N+S+E+W)





##### *************** GUI Post-Initialisation Code *************** #####

		
### ***** Rescale GUI size ***** ###
		
for x in range(4):
	Grid.columnconfigure(frame, x, weight = 1)

for y in range(22):
	Grid.rowconfigure(frame, y, weight = 1)



### ***** Post-initialisation code ***** ###
			
# Iterate the repetitive function call for data logging
root.after(60000, WriteToTextFile)
			
# Open a text file in writing "w" mode
# Note: opening in writing mode means that all data in the previous version of the file is overwritten
# Note: this is helpful as the text file can be restarted every time the GUI/session restarts
text_file = open("arbi7_text.txt", "w")

# Run the GUI until quitting
root.mainloop()
