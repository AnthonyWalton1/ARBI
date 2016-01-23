#!/usr/bin/env python

f = open("readTest.txt", 'r')

myList = []
char = ''

while char != '3':
	char = f.read(1)
	myList.append(char)
	
	
print myList
