#!/usr/bin/env python

# Import headers/modules
import serial
import ComsModule

handshakes = {}
machineState = {}
timers = {}
taskDictionary = {}
ComsVar = {}

GlobalComs = ComsModule.ComsClass()

updateHandshakesFromComs = True

handshakeMsgReceived = {"1" : {"P101" : False, "P102" : False, "P103" : False}, "2" : {"P101" : False, "P102" : False, "P103" : False}}

componentProtocolIDs = {"P101" : "001", "P102" : "002", "P103" : "003", "001" : "P101", "002" : "P102", "003" : "P103"}


