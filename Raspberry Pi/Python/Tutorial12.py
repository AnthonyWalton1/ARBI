#!/usr/bin/env python

from Tkinter import *
import tkMessageBox as box

root = Tk()

box.showinfo("Window Title", "Raspberry Pi")

answer = box.askquestion("Question 1", "Do you like Raspberry Pi?")

if answer == "yes":
	print("Yes")
	


root.mainloop()
