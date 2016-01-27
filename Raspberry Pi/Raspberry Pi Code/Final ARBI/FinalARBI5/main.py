#!/usr/bin/env python

# Import headers/modules
import time
import AI

def main():
	
	# Pause to let program initialise
	time.sleep(1)
	
	# Create object of control AI class from AI header. First object made so pass "1"
	# The corresponding GUI will be titled "ARBI GUI 1"
	ArbiAI = AI.AIclass("1")
	
	# Main loop (poll forever)
	while True:

		# Pause to slow down polling speed (for testing)
		time.sleep(1)
		
		# Measure all current values
		measurements = ArbiAI.status()
		
		# AI can decide what to do next based on measurements
		ArbiAI.decide(measurements)
		
		ArbiAI.AIserialWriteACM0("Msg for serial write\r\n")
		
		line = ArbiAI.AIserialReceiveACM0()
		print line
		
		ArbiAI.AIserialWriteACM1("Msg for serial write\r\n")
		
		line2 = ArbiAI.AIserialReceiveACM1()
		print line2

		# Log data
		ArbiAI.AIlogData(str(measurements))	

if __name__ == '__main__':
	main()
