#!/usr/bin/env python

from Tkinter import *
import time
import thread

# Part 1:
'''
def handle_click():
	print("Clicked!")

root = Tk()
Button(root, text = "Click me", command = handle_click).pack()
root.mainloop()
'''


# Part 2:
'''
def handle_click():
	win = Toplevel(root)
	win.transient()
	Label(win, text = "Please wait...").pack()
	for i in range(5, 0, -1):
		print(i)
		time.sleep(1)
	win.destroy()

root = Tk()
Button(root, text = "Click me", command = handle_click).pack()
root.mainloop()
'''

# Part 3: (not working)
'''
def handle_click():
	win = Toplevel()
	win.title("Hi")
	win.transient()
	Label(win, text = "Please wait...").pack()
	i = 5
	def callback():
		global i, win
		print(i)
		if not i:
			win.destroy()
		else:
			root.after(1000, callback)
	root.after(1000, callback)

root = Tk()
Button(root, text = "Click me", command = handle_click).pack()
root.mainloop()
'''

