#!/usr/bin/env python

numberOne = 1
ageofqueen = 78

def printhello():
	print "hello"
	
def timesfour(input):
	print input * 4

class Piano:
	def __init__(self):
		self.type = raw_input("What type of piano?")
		self.height = raw_input("What height?")
		self.price = raw_input("How much did it cost?")
		self.age = raw_input("How old is it?")
		
	def printdetails(self):
		print ("This piano is a " + self.height + "metre")
		print (self.type + " piano " + self.age + " years old that costs " + self.price + " dollars.")

class Pet:
	def __init__(self, name, species):
		self.name = name
		self.species = species
		
	def getName(self):
		return self.name
	
	def getSpecies(self):
		return self.species
