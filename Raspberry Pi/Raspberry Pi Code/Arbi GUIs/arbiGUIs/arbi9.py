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


# Function called for setting blue LED 1 luminosity and sending to Arduino
def BlueLed1Set():
		
	input = blueLed1Input.get()
		
	while (len(input) < 5):
		input = "0" + input
			
	print("14_" + input + "\r\n")
	ser.write("14_" + input + "\r\n")	



# Function called for setting blue LED 2 luminosity and sending to Arduino
def BlueLed2Set():

	input = blueLed2Input.get()
		
	while (len(input) < 5):
		input = "0" + input
			
	print("15_" + input + "\r\n")
	ser.write("15_" + input + "\r\n")	
			


# Function called for setting blue LED 3 luminosity and sending to Arduino
def BlueLed3Set():

	input = blueLed3Input.get()
		
	while (len(input) < 5):
		input = "0" + input
			
	print("16_" + input + "\r\n")
	ser.write("16_" + input + "\r\n")							
			


# Function called for setting red LED 1 luminosity and sending to Arduino		
def RedLed1Set():
		
	input = redLed1Input.get()
		
	while (len(input) < 5):
		input = "0" + input
			
	print("17_" + input + "\r\n")
	ser.write("17_" + input + "\r\n")	
					


# Function called for setting red LED 2 luminosity and sending to Arduino	
def RedLed2Set():

	input = redLed2Input.get()
		
	while (len(input) < 5):
		input = "0" + input
			
	print("18_" + input + "\r\n")
	ser.write("18_" + input + "\r\n")	
			


# Function called for setting red LED 3 luminosity and sending to Arduino	
def RedLed3Set():
		
	input = redLed3Input.get()
		
	while (len(input) < 5):
		input = "0" + input
			
	print("19_" + input + "\r\n")
	ser.write("19_" + input + "\r\n")	

			

# Function called for setting inside air temperature and sending to Arduino	
def InsideTempSet():

	input = insideTempInput.get()
		
	while (len(input) < 2):
		input = "0" + input
			
	print("09_" + input + "\r\n")
	ser.write("09_" + input + "\r\n")	
			
	

# Function called for setting water temperature and sending to Arduino
def WaterTempSet():

	input = waterTempInput.get()
		
	while (len(input) < 2):
		input = "0" + input
			
	print("10_" + input + "\r\n")
	ser.write("10_" + input + "\r\n")	
			


# Function called for setting LED on time and sending to Arduino
def LedOnTimeSet():
		
	if (flashStatusText.get() == "Flash"):
			
		input = str(int(float(ledOnTimeInput.get()) * 1000))
		
		while (len(input) < 7):
			input = "0" + input
		
		print("11_" + input + "\r\n")
		ser.write("11_" + input + "\r\n")
		


# Function called for setting LED off time and sending to Arduino
def LedOffTimeSet():

	if (flashStatusText.get() == "Flash"):
			
		input = str(int(float(ledOffTimeInput.get()) * 1000))
		
		while (len(input) < 7):
			input = "0" + input
		
		print("12_" + input + "\r\n")
		ser.write("12_" + input + "\r\n")
	


# Function called for changing LED frequency text description in Entry Boxes and Labels
def FlashStatusToggle():
	
	# If statement to execute toggling process 
	# Note: sequence is: from Flash (initially) to On to Off and back to Flash, repeated
	
	if (flashStatusText.get() == "Flash"):
			
		flashStatusText.set("On")
			
		ledOnTimeInput.delete(0, END)
		ledOnTimeInput.insert(END, "On")

		ledOffTimeInput.delete(0, END)
		ledOffTimeInput.insert(END, "On")
		
		print("13_1\r\n")
		ser.write("13_1\r\n")
			
	elif (flashStatusText.get() == "On"):
			
		flashStatusText.set("Off")
			
		ledOnTimeInput.delete(0, END)
		ledOnTimeInput.insert(END, "Off")
			
		ledOffTimeInput.delete(0, END)
		ledOffTimeInput.insert(END, "Off")
		
		print("13_2\r\n")
		ser.write("13_2\r\n")
			
	else:
			
		flashStatusText.set("Flash")
			
		ledOnTimeInput.delete(0, END)
		ledOnTimeInput.insert(END, "1")
			
		ledOffTimeInput.delete(0, END)
		ledOffTimeInput.insert(END, "1")
		
		print("13_0\r\n")
		ser.write("13_0\r\n")
		
		# Also send signal for default on time = 1 and off time = 1 when toggled back to flash mode
		LedOnTimeSet()
		LedOffTimeSet()



# Function for sending signal to receive data from Arduino
def SendBuffer():

	# Send the signal to the Arduino to send the Raspberry Pi all data
	ser.write("99_000\r\n")
		
	# Wait for the data to be received from the Arduino
	time.sleep(2)
	
	

# Function for saving Arduino data into an input string.
# Returns input string 'line'
def ReceiveBuffer():
	
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
	print("\r\n\r\n" + line + "\r\n")
	
	# Return line variable to function call
	return line

		
			
# Function called for writing to the text file
def WriteToTextFile():

	# Open the text file each time since we close it each time
	# Note: "a" means opening the text file in append mode. 
	# Note: This is required as "w" writing mode overwrites the previous file once it is closed an re-opened.
	# Note: we want to add the next set of data to the pre-existing list, which is what append mode does.
	text_file = open("arbi9_text.txt", "a")
		
	# Send signal to receive data from Arduino
	SendBuffer()
	
	# Call this function to run again
	# Note: this is a self-iterating process
	root.after(10000, WriteToTextFile)
	
	# Receive data from Arduino into an input string
	line = ReceiveBuffer()
	
	# Call error checking function without updating current values
	# Note: the final enter \r\n contributes 1 unit to the length of the line
	error = ErrorCheck(line)
	
	# Log data if no errors occured
	if error == 0:
		
		# Split the input string at the spaces to separate data
		values = line.split(" ")
		
		# Extract data
		
		# Put temperature data into decimal format
		insideTempSensor1 = values[0].split("_")[1][0] + values[0].split("_")[1][1] + \
		"." + values[0].split("_")[1][2] + values[0].split("_")[1][3]
		insideTempSensor2 = values[1].split("_")[1][0] + values[1].split("_")[1][1] + \
		"." + values[1].split("_")[1][2] + values[1].split("_")[1][3]
		insideTempSensor3 = values[2].split("_")[1][0] + values[2].split("_")[1][1] + \
		"." + values[2].split("_")[1][2] + values[2].split("_")[1][3]
		insideTempSensor4 = values[3].split("_")[1][0] + values[3].split("_")[1][1] + \
		"." + values[3].split("_")[1][2] + values[3].split("_")[1][3]
		insideTempSensor5 = values[4].split("_")[1][0] + values[4].split("_")[1][1] + \
		"." + values[4].split("_")[1][2] + values[4].split("_")[1][3]
		insideTempSensor6 = values[5].split("_")[1][0] + values[5].split("_")[1][1] + \
		"." + values[5].split("_")[1][2] + values[5].split("_")[1][3]
		waterTempSensor1 = values[6].split("_")[1][0] + values[6].split("_")[1][1] + \
		"." + values[6].split("_")[1][2] + values[6].split("_")[1][3]
		waterTempSensor2 = values[7].split("_")[1][0] + values[7].split("_")[1][1] + \
		"." + values[7].split("_")[1][2] + values[7].split("_")[1][3]
		
		blueLed1 = values[19].split("_")[1]
		blueLed2 = values[20].split("_")[1]
		blueLed3 = values[21].split("_")[1]
		redLed1 = values[22].split("_")[1]
		redLed2 = values[23].split("_")[1]
		redLed3 = values[24].split("_")[1]
		
		flowRate = values[31].split("_")[1]
		
		seconds = values[25].split("_")[1]
		minutes = values[26].split("_")[1]
		hours = values[27].split("_")[1]
		days = values[28].split("_")[1]
		months = values[29].split("_")[1]
		years = values[30].split("_")[1]		
				
		# Convert all external RTC component time values to seconds
		secondsData = str(int(seconds) + int(minutes)*60 + \
		int(hours)*60*60 + int(days)*60*60*24+int(months)*60*60*24*12 + \
		int(years)*60*60*24*12*365)
		
		# Concatentate the string in comma separated format for Excel
		# Note: enter means a new row in Excel (no choice)
		# Note: comma means a new column in Excel (choice, could also be a tab, etc)
		# Note: data structure wrt columns is (time, value) for Excel graphing
		msg = secondsData + "," + insideTempSensor1 + ',' + insideTempSensor2 + \
		',' + insideTempSensor3 + ',' + insideTempSensor4 + ',' + insideTempSensor5 + \
		',' + insideTempSensor6 + ',' + waterTempSensor1 + ',' + waterTempSensor2 + \
		',' + blueLed1 + ',' + blueLed2 + ',' + blueLed3 + ',' + redLed1 + ',' + redLed2 + \
		',' + redLed3 + ',' + flowRate + "\r\n"
	
		# Print the message for verification
		print("\r\n" + msg)
	
		# Write the data with the correct format into the file
		text_file.write(msg)
	
		# Close the file each time so that the writing is saved
		text_file.close()
		
	
	

# Function for updating the current values on the GUI
def UpdateCurrentValues():
	
	# Send signal to tell Arduino to send data
	SendBuffer()
	
	# Receive data from Arduino into an input string
	line = ReceiveBuffer()
	
	# Call Error Check and updae GUI values
	# Note: the final enter \r\n contributes 1 unit to the length of the line
	error = ErrorCheck(line)
	
	# Update current values on GUI if no errors occured
	if error == 0:
		
		# Split the input string at the spaces to separate data
		values = line.split(" ")
		
		# Update data
		insideTemp1Text.set(values[0].split("_")[1][0] + values[0].split("_")[1][1] + \
		"." + values[0].split("_")[1][2] + values[0].split("_")[1][3])
		insideTemp2Text.set(values[1].split("_")[1][0] + values[1].split("_")[1][1] + \
		"." + values[1].split("_")[1][2] + values[1].split("_")[1][3])
		insideTemp3Text.set(values[2].split("_")[1][0] + values[2].split("_")[1][1] + \
		"." + values[2].split("_")[1][2] + values[2].split("_")[1][3])
		insideTemp4Text.set(values[3].split("_")[1][0] + values[3].split("_")[1][1] + \
		"." + values[3].split("_")[1][2] + values[3].split("_")[1][3])
		insideTemp5Text.set(values[4].split("_")[1][0] + values[4].split("_")[1][1] + \
		"." + values[4].split("_")[1][2] + values[4].split("_")[1][3])
		insideTemp6Text.set(values[5].split("_")[1][0] + values[5].split("_")[1][1] + \
		"." + values[5].split("_")[1][2] + values[5].split("_")[1][3])
		waterTemp1Text.set(values[6].split("_")[1][0] + values[6].split("_")[1][1] + \
		"." + values[6].split("_")[1][2] + values[6].split("_")[1][3])
		waterTemp2Text.set(values[7].split("_")[1][0] + values[7].split("_")[1][1] + \
		"." + values[7].split("_")[1][2] + values[7].split("_")[1][3])
		
		blueLed1Text.set(values[19].split("_")[1])
		blueLed2Text.set(values[20].split("_")[1])
		blueLed3Text.set(values[21].split("_")[1])
		redLed1Text.set(values[22].split("_")[1])
		redLed2Text.set(values[23].split("_")[1])
		redLed3Text.set(values[24].split("_")[1])
		
		flowMeterText.set(values[31].split("_")[1])
	


# Function for performing an error check on the serial communication input
def ErrorCheck(line):
	
	# Split the input string at the spaces to separate data
	values = line.split(" ")
			
	# Reset error flag to off (no errors unless otherwise encountered)
	error = 0
	
	# Check total length of line to ensure indexing line does not exceed what exists
	if len(line) == 254:
		print("correct length")
		
		# Check that spaces and underscores are in the correct places so that indexing them
		# in GUI updating and data logging does not exceed what exists
		
		# Print an error message relevant to each section of the serial string
		# This assists in pinpointing regions of error in a large input string
			
		if line[2] == "_":
			print("01 correct")
		else:
			print("Return string: wrong format 01")
			error = 1
			
		if line[7] == " " and line[10] == "_":
			print("02 correct")
		else:
			print("Return string: wrong format 02")
			error = 1
			
		if line[15] == " " and line[18] == "_":
			print("03 correct")
		else:
			print("Return string: wrong format 03")
			error = 1
		
		if line[23] == " " and line[26] == "_":
			print("04 correct")
		else:
			print("Return string: wrong format 04")
			error = 1
		
		if line[31] == " " and line[34] == "_":
			print("05 correct")
		else:
			print("Return string: wrong format 05")
			error = 1
		
		if line[39] == " " and line[42] == "_":
			print("06 correct")
		else:
			print("Return string: wrong format 06")
			error = 1		
		
		if line[47] == " " and line[50] == "_":
			print("07 correct")
		else:
			print("Return string: wrong format 07")
			error = 1
					
		if line[55] == " " and line[58] == "_":
			print("08 correct")
		else:
			print("Return string: wrong format 08")
			error = 1
		
		if line[63] == " " and line[66] == "_":
			print("09 correct")
		else:
			print("Return string: wrong format 09")
			error = 1
	
		if line[69] == " " and line[72] == "_":
			print("10 correct")
		else:
			print("Return string: wrong format 10")
			error = 1
	
		if line[75] == " " and line[78] == "_":
			print("11 correct")
		else:
			print("Return string: wrong format 11")
			error = 1
		
		if line[86] == " " and line[89] == "_":
			print("12 correct")	
		else:
			print("Return string: wrong format 12")
			error = 1
			
		if line[97] == " " and line[100] == "_":
			print("13 correct")
		else:
			print("Return string: wrong format 13")
			error = 1
			
		if line[102] == " " and line[105] == "_":
			print("14 correct")
		else:
			print("Return string: wrong format 14")
			error = 1
			
		if line[111] == " " and line[114] == "_":
			print("15 correct")
		else:
			print("Return string: wrong format 15")
			error = 1
			
		if line[120] == " " and line[123] == "_":
			print("16 correct")
		else:
			print("Return string: wrong format 16")
			error = 1
			
		if line[129] == " " and line[132] == "_":
			print("17 correct")
		else:
			print("Return string: wrong format 17")
			error = 1
			
		if line[138] == " " and line[141] == "_":
			print("18 correct")
		else:
			print("Return string: wrong format 18")
			error = 1
			
		if line[147] == " " and line[150] == "_":
			print("19 correct")
		else:
			print("Return string: wrong format 19")
			error = 1
			
		if line[156] == " " and line[159] == "_":
			print("20 correct")
		else:
			print("Return string: wrong format 20")
			error = 1

		if line[165] == " " and line[168] == "_":
			print("21 correct")
		else:
			print("Return string: wrong format 21")
			error = 1
			
		if line[174] == " " and line[177] == "_":
			print("22 correct")
		else:
			print("Return string: wrong format 22")
			error = 1
			
		if line[183] == " " and line[186] == "_":
			print("23 correct")
		else:
			print("Return string: wrong format 23")
			error = 1
			
		if line[192] == " " and line[195] == "_":
			print("24 correct")
		else:
			print("Return string: wrong format 24")
			error = 1
			
		if line[201] == " " and line[204] == "_":
			print("25 correct")
		else:
			print("Return string: wrong format 25")
			error = 1
						
		if line[210] == " " and line[213] == "_":
			print("26 correct")
		else:
			print("Return string: wrong format 26")
			error = 1
			
		if line[216] == " " and line[219] == "_":
			print("27 correct")
		else:
			print("Return string: wrong format 27")
			error = 1
			
		if line[222] == " " and line[225] == "_":
			print("28 correct")
		else:
			print("Return string: wrong format 28")
			error = 1
			
		if line[228] == " " and line[231] == "_":
			print("29 correct")
		else:
			print("Return string: wrong format 29")
			error = 1
			
		if line[234] == " " and line[237] == "_":
			print("30 correct")
		else:
			print("Return string: wrong format 30")
			error = 1
			
		if line[240] == " " and line[243] == "_":
			print("31 correct")
		else:
			print("Return string: wrong format 31")
			error = 1
			
		if line[246] == " " and line[249] == "_":
			print("32 correct")
		else:
			print("Return string: wrong format 32")
			error = 1
							
	else:
		print("Return string: wrong length")
		error = 1
		
	# If any errors occured at all print an error flag
	if error == 1:
		print("Error Flag")	
	
	# Return error variable to function call
	return error




	
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
flowMeterText = StringVar()
flowMeterLabel = Label(frame, textvariable = flowMeterText, bg = "white")
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
		
updateCurValButton = Button(frame, text = "Update Current Values", command = UpdateCurrentValues)
updateCurValButton.grid(row = 21, column = 0, columnspan = 4, sticky = N+S+E+W)





##### *************** GUI Post-Initialisation Code *************** #####

		
### ***** Rescale GUI size ***** ###
		
for x in range(4):
	Grid.columnconfigure(frame, x, weight = 1)

for y in range(22):
	Grid.rowconfigure(frame, y, weight = 1)



### ***** Post-initialisation code ***** ###
			
# Initialise the repetitive function call for data logging
root.after(10000, WriteToTextFile)
			
# Open a text file in writing "w" mode
# Note: opening in writing mode means that all data in the previous version of the file is overwritten
# Note: this is helpful as the text file can be restarted every time the GUI session restarts
text_file = open("arbi9_text.txt", "w")

# Run the GUI until quitting
root.mainloop()
