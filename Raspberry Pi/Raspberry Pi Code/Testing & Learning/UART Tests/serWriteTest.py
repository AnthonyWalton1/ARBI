#!/usr/bin/env python

import serial
import time
import threading
ser = serial.Serial('/dev/ttyACM0', 9600)

'''
# Part 1: Echoing String code:

time.sleep(1)
ser.write("Message sent over Serial\r\n")


while msgEnd == 0:
	if ser.inWaiting() != 0:
		val = ser.read(1)

		if ((val != "\r") and (val != "\n")):
			line += val
			
		if val == "\n":
			msgEnd = 1
			print line
'''			

'''
# Part 2: Testing variable scopes between main (in 2 different forms) and thread.
# Also testing if just thread can ser.write, just main, and main and thread

# THREAD AS A CLASS

class serialWrite(threading.Thread):
	def __init__(self, text):
		threading.Thread.__init__(self)
		self.text = text
		
	def run(self):
		time.sleep(0.1)
		print "thread run fxn working"
		testString2 = "variable defined in thread is seen in main"
		try:
			print testString1
		except:
			print "variable defined in main isnt seen in thread"		
		
		
		ser.write(self.text)
		print "serial write working"
		
		msgEnd = 0;
		line = ""
		
		while msgEnd == 0:
			if ser.inWaiting() != 0:
				val = ser.read(1)

				if ((val != "\r") and (val != "\n")):
					line += val
					
				if val == "\n":
					msgEnd = 1
					print line + " returned"
		
		time.sleep(5)	
				
		

time.sleep(1)
serThread1 = serialWrite("Message to send over serial\r\n")
serThread1.start()
print "The program can continue to run while it writes in another thread"
print str(100 + 400)
testString1 = "variable defined in main is seen in thread"


for i in range(1,10):
	ser.write(str(i) + ": msg sent over serial from main\r\n")
		
	msgEnd1 = 0;
	line1 = ""
			
	while msgEnd1 == 0:
		if ser.inWaiting() != 0:
			val1 = ser.read(1)

			if ((val1 != "\r") and (val1 != "\n")):
				line1 += val1
							
			if val1 == "\n":
				msgEnd1 = 1
				print line1 + " returned"


try:
	print testString2
except:
	print "variable defined in thread isnt seen in main"
	
serThread1.join()
print "Waited until thread was complete"
'''


'''
# Part 3: Testing variable scopes between main (in 2 different forms) and thread.
# Also testing if just thread can ser.write, just main, and main and thread

# THREAD AS A FUNCTION

def testThread(text):
		time.sleep(0.1)
		print "thread run fxn working"
		testString2 = "variable defined in thread is seen in main"
		try:
			print testString1
		except:
			print "variable defined in main isnt seen in thread"		
		
		
		ser.write(text)
		print "serial write working"
		
		msgEnd = 0;
		line = ""
		
		while msgEnd == 0:
			if ser.inWaiting() != 0:
				val = ser.read(1)

				if ((val != "\r") and (val != "\n")):
					line += val
					
				if val == "\n":
					msgEnd = 1
					print line + " returned"
		
		time.sleep(5)

		

time.sleep(1)
serThread1 = threading.Thread(target = testThread, args=("Message to send over serial\r\n",))
serThread1.start()
print "The program can continue to run while it writes in another thread"
print str(100 + 400)
testString1 = "variable defined in main is seen in thread"


for i in range(1,10):
	ser.write(str(i) + ": msg sent over serial from main\r\n")
		
	msgEnd1 = 0;
	line1 = ""
			
	while msgEnd1 == 0:
		if ser.inWaiting() != 0:
			val1 = ser.read(1)

			if ((val1 != "\r") and (val1 != "\n")):
				line1 += val1
							
			if val1 == "\n":
				msgEnd1 = 1
				print line1 + " returned"


try:
	print testString2
except:
	print "variable defined in thread isnt seen in main"
	
serThread1.join()
print "Waited until thread was complete"
'''



# Part 3: Testing serial as separate thread

def serialWrite(text):
	
	serialLock.acquire()
	
	ser.write(text)
	
	msgEnd = 0;
	line = ""
		
	while msgEnd == 0:
		if ser.inWaiting() != 0:
			val = ser.read(1)

			if ((val != "\r") and (val != "\n")):
				line += val
					
			if val == "\n":
				msgEnd = 1
				print line + " returned"	
	
	serialLock.release()


def testThread(threadName):
	while True:
		
		print threadName + "working"
		serialWrite("Msg sent over serial from" + threadName + "\r\n")
		time.sleep(0.8)
		
		

serialLock = threading.Lock()		

time.sleep(1)
serThread1 = threading.Thread(target = testThread, args = ("Thread 1",))
serThread1.start()

serThread2 = threading.Thread(target = testThread, args = ("Thread 2",))
serThread2.start()


while True:
	for i in range(1, 101):
		serialWrite("Msg sent over serial from main\r\n")
		
	time.sleep(1)



