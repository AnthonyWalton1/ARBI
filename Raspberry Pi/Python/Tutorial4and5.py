#!/usr/bin/env python

from Tkinter import *

root = Tk()

label_1 = Label(root, text = "Name")
label_2 = Label(root, text = "Password")

entry_1 = Entry(root)
entry_2 = Entry(root)


label_1.grid(row = 0, column = 0, sticky = E)	# Don't need column = 0 as it is 0 be default
label_2.grid(row = 1, column = 0, sticky = E)	# Don't need column = 0 as it is 0 be default

# N, E, S, W for north south east west

entry_1.grid(row = 0, column = 1)
entry_2.grid(row = 1, column = 1)

c = Checkbutton(root, text = "Keep me logged in")

c.grid(row = 2, columnspan = 2)	# Row = 2 seems to be optional, might take the highest free line



root.mainloop()
