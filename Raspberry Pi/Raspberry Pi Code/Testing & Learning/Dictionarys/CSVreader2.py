#!/usr/bin/env python



#!/usr/bin/env python

import time
import csv

# Read flow diagram file
readerFATflow = csv.DictReader(open('FATflow.csv'))

FATflow = {}
for row in readerFATflow:
	key = row.pop('Flow')
	if key in FATflow:
		pass
	FATflow[key] = row
print FATflow

# Read task diagram file
readerFATtask = csv.DictReader(open('FATtask.csv'))

FATtask = {}
for row in readerFATtask:
	key = row.pop('Step')
	if key in FATtask: 
		print "hi"
		pass
	FATtask[key] = row
print FATtask

# Create ascending order array for indexing flow table
arrayFATflow = []
for i in range(1, len(FATflow) + 1):
	arrayFATflow.append(str(i))
	
arrayFATtask = []
for i in range(1, len(FATtask) + 1):
	arrayFATtask.append(str(i))
	



























measurements = {}
measurements["FL301"] = "0"
measurements["FCV301"] = "0"
measurements["V201a"] = "0"
measurements["V201b"] = "0"
measurements["V301"] = "0"
measurements["V302"] = "0"


def millis():
	return int(round(time.time() * 1000))


def hasTimePassed(refTime, timeWait):
	
	if refTime == "HAT":
		timedif = millis() - HATstart

		if timedif/1000 > int(timeWait)/100:
			print "time yes"
			return "Yes"
		else:
			print "time no"
			return "No"
		
def sensorReading(sensorID, reqVal):
	
	measuredVal = measurements[sensorID]

	if (int(measuredVal) > int(reqVal)):
		print "sensor yes"
		return "Yes"
	else:
		print "sensor no"
		return "No"

def conditionFxnFlow(fxnFlag, i):
	
	if fxnFlag == "hasTimePassed":
		tf = hasTimePassed(FATflow[i]["ConditionValues"].split("_")[0], \
		FATflow[i]["ConditionValues"].split("_")[1])
		
		
	if fxnFlag == "sensorReading":
		tf = sensorReading(FATflow[i]["ConditionValues"].split("_")[0], \
		FATflow[i]["ConditionValues"].split("_")[1])
	
	return tf
	
def conditionFxnTask(fxnFlag, value, a):
	
	if fxnFlag == "OpenClose":
		print a + "_" + value




HATstart = millis()
timerstart = millis()
i = arrayFATflow[0]
areMeasurementsCorrect = {}
measurementWait = 0


while True: 

	if (int(i) <= len(arrayFATflow)):

		time.sleep(5)
		
		if millis() - timerstart > 20*1000:
			timerstart = millis()
			for a in FATtask[FATflow[i]["Yes"]]:
				measurements[a] = int(FATtask[FATflow[i]["Yes"]][a].split("_")[1])
				
				if millis() - HATstart > 60*1000:
					measurements["FL301"] = 1000
					
				if millis() - HATstart > 100*1000:
					measurements["FL301"] = 10000
		
		if measurementWait == 0:
			print "hi"
			
			tf = conditionFxnFlow(FATflow[i]["ConditionFxn"], i)

			if FATflow[i][tf] != "#":

				for a in FATtask[FATflow[i]["Yes"]]:
					
					conditionFxnTask(FATtask[FATflow[i]["Yes"]][a].split("_")[0], \
					FATtask[FATflow[i]["Yes"]][a].split("_")[1], a)
					
					if int(FATtask[FATflow[i]["Yes"]][a].split("_")[1]) == int(measurements[a]):
						
						areMeasurementsCorrect[a] = 1
					
					else:
						
						areMeasurementsCorrect[a] = 0	

				if  all(areMeasurementsCorrect[x] == 1 for x in areMeasurementsCorrect) == 1:
							
					i = str(int(i) + 1)
					measurementWait = 0
					print "yes1"
				
				else:
					
					measurementWait = 1
					print "no1"
					
		else:
			
			for a in FATtask[FATflow[i]["Yes"]]:

				if int(FATtask[FATflow[i]["Yes"]][a].split("_")[1]) == int(measurements[a]):
					
					areMeasurementsCorrect[a] = 1
				
				else:
					
					areMeasurementsCorrect[a] = 0
		
			if all(areMeasurementsCorrect[x] == 1 for x in areMeasurementsCorrect) == 1:
						
				i = str(int(i) + 1)
				measurementWait = 0
				print "yes2"
			
			else:
				print "no2"
				measurementWait = 1	
				
						
	else:
		time.sleep(1)
		print "finished"
		pass
	

	

