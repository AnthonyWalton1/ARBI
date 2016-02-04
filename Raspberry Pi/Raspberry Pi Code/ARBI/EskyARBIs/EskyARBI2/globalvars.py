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
