#!/usr/bin/env python

from Tkinter import *

root = Tk()

d = StringVar()

label = Label(root, text = "Result is: ")
result = Label(root, textvariable = d)

a = StringVar()
b = StringVar()

e = Entry(root, textvariable = a)
e2 = Entry(root, textvariable = b)

def add():
	added = int(a.get()) + int(b.get())
	d.set(added)

e.pack()
e2.pack()
button = Button(root, text = "Add", command = add)
button.pack()
label.pack()
result.pack()
root.mainloop()
