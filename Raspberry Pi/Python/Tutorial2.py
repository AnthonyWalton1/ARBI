#!/usr/bin/env python

from Tkinter import *

# Start a GUI (object) from Tkinter class
root = Tk()

topFrame = Frame(root)
topFrame.pack(side = TOP) #Note: by default it places it on top first, so could just use topFrame.pack()

bottomFrame = Frame(root)
bottomFrame.pack(side = BOTTOM)

button1 = Button(topFrame, text = "Button 1", fg = "red")
button2 = Button(topFrame, text = "Button 2", fg = "blue")
button3 = Button(topFrame, text = "Button 3", fg = "green")
button4 = Button(bottomFrame, text = "Button 4", fg = "purple")


button1.pack(side = LEFT)
button2.pack(side = LEFT)
button3.pack(side = LEFT)
button4.pack(side = BOTTOM)

# Keep the GUI on screen
root.mainloop()


