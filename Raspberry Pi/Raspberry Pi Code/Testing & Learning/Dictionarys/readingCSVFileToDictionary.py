#!/usr/bin/env python

import time
import csv

reader = csv.DictReader(open('test2.csv'))
'''
result = {}
for row in reader:
	for column, value in row.iteritems():
		result.setdefault(column, []).append(value)
print result
'''
'''
#for i in result:
#	for a in result[i]:
#		print i, result[i][a]


result = {}
for row in reader:
	key = row.pop('1')
	if key in result:
		pass
	result[key] = row
print result

array = []
for i in result:
	array.append(i)

array = sorted(array)			

dict = {}
for i in array:
	dict[i] = result[i]
	print dict
	
print dict	
	
#for i in result:
#	for a in result[i]:
#		print i, result[i][a]


'''

# Read flow diagram file
readerFATflow = csv.DictReader(open('FATflow.csv'))

resultFATflow = {}
for row in readerFATflow:
	key = row.pop('Flow')
	if key in resultFATflow:
		pass
	resultFATflow[key] = row
print resultFATflow


# Read task diagram file
readerFATtask = csv.DictReader(open('FATtask.csv'))

resultFATtask = {}
for row in readerFATtask:
	key = row.pop('Step')
	if key in resultFATtask: 
		print "hi"
		pass
	resultFATtask[key] = row
print resultFATtask


# Create ascending order array for indexing flow table
arrayFATflow = []
for i in range(1, len(resultFATflow) + 1):
	arrayFATflow.append(str(i))
	print arrayFATflow
	
arrayFATtask = []
for i in range(1, len(resultFATtask) + 1):
	arrayFATtask.append(str(i))
	print arrayFATtask

measurements = {}
measurements["FL301"] = 45


def millis():
	return int(round(time.time() * 1000))


def hasTimePassed(refTime, timeWait):
	
	if refTime == "HAT":
		timedif = millis() - HATstart

		if timedif/1000 > int(timeWait)/100:
			return "Yes"
		else:
			return "No"
		
def sensorReading(sensorID, reqVal):
	
	measuredVal = measurements[sensorID]

	if (int(measuredVal) > int(reqVal)/4):
		return "Yes"
	else:
		return "No"

def conditionFxnFlow(fxnFlag, i):
	
	if fxnFlag == "hasTimePassed":
		tf = hasTimePassed(resultFATflow[i]["ConditionValues"].split("_")[0], \
		resultFATflow[i]["ConditionValues"].split("_")[1])
		
		
	if fxnFlag == "sensorReading":
		tf = sensorReading(resultFATflow[i]["ConditionValues"].split("_")[0], \
		resultFATflow[i]["ConditionValues"].split("_")[1])
	
	return tf
	
def conditionFxnTask(fxnFlag, value, a):
	
	if fxnFlag == "OpenClose":
		print a + "_" + value




HATstart = millis()
i = arrayFATflow[0]


while True:
	
	if (int(i) <= len(arrayFATflow)):
		
		time.sleep(1)
		
		tf = conditionFxnFlow(resultFATflow[i]["ConditionFxn"], i)
		
		if resultFATflow[i][tf] != "#":
			
			for a in resultFATtask[resultFATflow[i]["Yes"]]:
				
				conditionFxnTask(resultFATtask[resultFATflow[i]["Yes"]][a].split("_")[0], \
				resultFATtask[resultFATflow[i]["Yes"]][a].split("_")[1], a)
				
			i = str(int(i) + 1)
			
		else:
			
			pass

				
	#measurements["FL301"] = (millis() - HATstart)/1000


