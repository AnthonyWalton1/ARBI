#!/usr/bin/env python


from Tkinter import *

class RaspberryPisButtons:
	
	# This function stands for initialise and runs automatically whenever a new object is created
	def __init__(self, master):
		frame = Frame(master)
		frame.pack()
		
		self.printButton = Button(frame, text = "Print Message", command = self.printMessage)
		self.printButton.pack(side = LEFT)
		
		self.quitButton = Button(frame, text = "Quit", command = frame.quit)	# frame.quit is already an inbuilt function, it breaks the main loop
		self.quitButton.pack(side = LEFT)
		
	def printMessage(self):
		print("Tutorial 8 for GUIs in Python")
		

root = Tk()

# Create an object called b, pass the 'root' instance of the 'master'
b = RaspberryPisButtons(root)

root.mainloop()
