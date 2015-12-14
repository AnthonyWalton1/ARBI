#!/usr/bin/env python

# Shows how to write a text file

# ***** METHOD 1 ***** #

print("Creating a text file with the write() method")

# First you must open the file and give it a file name
# Note the text file can be opened on Leafpad, Notepad, etc
text_file = open("write_it.txt", "w") # w stands for open in writing mode i.e. we want to write to the file

# Write to the file
text_file.write("Line 1\r\nThis is Line 2\r\nThis is line 3\r\n")

# Must close the file when finished
text_file.close()


# Can reopen file in read mode
text_file = open("write_it.txt", "r")

# Print what the file contains (read with no arguments reads whole file)
print(text_file.read())

# Close the file when finished
text_file.close()


# ***** METHOD 2 ***** #

print("\r\n\r\n\r\n")
print("Create a text file with writelines() method")

text_file = open("write_it.txt", "w")

lines = ["Line 1\r\n", "Line 2\r\n", "This is Line 3\r\n"]

text_file.writelines(lines)
text_file.close()

text_file = open("write_it.txt", "r")
print(text_file.read())
text_file.close()
