#!/usr/bin/env python

# Import headers/modules
import time
import AI
import globalvariables


def main():	
	time.sleep(2)
	
	globalvariables.init()
	ArbiAI = AI.AIclass("1")
	
	print globalvariables.handshakes
	print globalvariables.machineState

	ArbiAI.AIserialWrite("1_Msg for serial write1_ACM1\r\n")
	time.sleep(3)
	ArbiAI.AIserialReceive()
	print globalvariables.handshakes
	print globalvariables.machineState

	ArbiAI.AIserialWrite("1_Msg for serial write_ACM0\r\n")	
	time.sleep(3)
	ArbiAI.AIserialReceive()
	print globalvariables.handshakes
	print globalvariables.machineState

	ArbiAI.AIserialWrite("1_Hi again_ACM0\r\n")
	time.sleep(3)
	ArbiAI.AIserialReceive()
	print globalvariables.handshakes
	print globalvariables.machineState

	ArbiAI.AIserialWrite("1_Hi again2_ACM0\r\n")
	time.sleep(3)
	ArbiAI.AIserialReceive()
	print globalvariables.handshakes
	print globalvariables.machineState

	ArbiAI.AIserialWrite("1_Hi again3_ACM0\r\n")	
	time.sleep(3)
	ArbiAI.AIserialReceive()
	print globalvariables.handshakes
	print globalvariables.machineState


	while True:
		time.sleep(1)
		
		measurements = ArbiAI.status()
		ArbiAI.decide(measurements)
		

if __name__ == '__main__':
	main()
