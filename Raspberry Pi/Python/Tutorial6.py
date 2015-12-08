#!/usr/bin/env python



''' Method 1:
from Tkinter import *

root = Tk()

def printName():
	print("Hello my name is Raspberry Pi")

button_1 = Button(root, text = "Print my name", command = printName)
button_1.pack()


root.mainloop()
'''

''' Method 2: '''
from Tkinter import *

root = Tk()

def printName(event):
	print("Hello my name is Raspberry Pi")

button_1 = Button(root, text = "Print my name")
button_1.bind("<Button-1>", printName)	#"<Button-1>" is the event name for a left mouse click
button_1.pack()

root.mainloop()
