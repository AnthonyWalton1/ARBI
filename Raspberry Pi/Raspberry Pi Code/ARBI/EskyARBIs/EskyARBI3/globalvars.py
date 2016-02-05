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

handshakeMsgReceived = {"P101" : False, "P102" : False, "P103" : False}
