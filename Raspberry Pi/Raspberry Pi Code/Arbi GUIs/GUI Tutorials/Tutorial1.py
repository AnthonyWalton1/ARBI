#!/usr/bin/env python

from Tkinter import *

# Start a GUI (object) from Tkinter class
root = Tk()


# Create a label (text box widget) called theLabel and set what text it shows
theLabel = Label(root, text = "Python GUI")

# Place the text box in the first available space and display it
theLabel.pack()


# Keep the GUI on screen
root.mainloop()

