#!/usr/bin/env python

from Tkinter import *

def doNothing():
	print("Do Nothing")

root = Tk()

# **** Main Menu ****

# Personal name of 'menu'
mainMenu = Menu(root)

# Parameter name is menu on the left. In this case, paramenter and personal name are the same
root.config(menu = mainMenu)

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label = "File", menu = fileMenu)
fileMenu.add_command(label = "New Project ...", command = doNothing)
fileMenu.add_command(label = "New ...", command = doNothing)
fileMenu.add_separator()
fileMenu.add_command(label = "Exit", command = root.quit)

editMenu = Menu(mainMenu)
mainMenu.add_cascade(label = "Edit", menu = editMenu)
editMenu.add_command(label = "Redo", command = doNothing)



# **** Toolbar ****

toolbar = Frame(root, bg = "blue")

insertButton = Button(toolbar, text = "Insert Image", command = doNothing)
insertButton.pack(side = LEFT, padx = 2, pady = 2)

printButton = Button(toolbar, text = "Print", command = doNothing)
printButton.pack(side = LEFT, padx = 2, pady = 2)

# Automatically positons directly underneath main Menu by using TOP
toolbar.pack(side = TOP, fill = X)



# **** Status Bar ****

#bd stands for border, relief means how the border will appear visually
status = Label(root, text = "GUI using Python...", bd = 1, relief = SUNKEN, anchor = W) # W = west = left
status.pack(side = BOTTOM, fill = X)


root.mainloop()
