#!/usr/bin/env python

def defineDict(florida):
	
	a = 2
	states = {"Oregon": "OR", "Florida": florida}
	
	states["New York"] = "NY"
	
	states["California"] = "CA"
	
	states["Michigan"] = a
	
	return states
	
	
dictionary = defineDict("FL")

print dictionary["Oregon"]
print dictionary["Florida"]
print dictionary["Michigan"]

