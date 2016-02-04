#!/usr/bin/env python

# Import headers/modules
import threading
import time
import GUI
import UART
import DataLogger
import AI

def main():
	
	# Pause to let program initialise
	time.sleep(1)
	
	# Create object of GUIclass from GUI header and create a thread that runs the createGUI function from that class
	
	ArbiGUI = GUI.GUIclass()
	guiThread = threading.Thread(target = ArbiGUI.createGUI)
	guiThread.start()
	
	# Create object of data logging class from DataLogger header. Erases data from file name if it exists from last user
	ArbiDataLogger = DataLogger.DataLoggerClass("maintextfile.txt")
	ArbiDataLogger.clearFile()
	
	# Create object of control AI class from AI header
	ArbiAI = AI.AiClass()

	
	# Main loop
	while True:
		time.sleep(0.5)
		ArbiAI.status()
		
		ArbiAI.decide()
		
		state = ArbiGUI.getBlueLED1State()

		print state

		line = UART.serialWrite("hlhjlj\r\n",)		
		
		ArbiDataLogger.logData(line)
		

if __name__ == '__main__':
	main()
