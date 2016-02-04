#!/usr/bin/env python

# Import headers/modules
import time
import AI
import globalvars
import globalfxns


def main():	
	time.sleep(2)

	HATstarttime = globalfxns.millis()

	globalvars.timers = {"HAT" : HATstarttime}
	globalvars.machineState = {"FCV301" : "0", "V201a" : "0", "V201b" :"0", "V301" : "0", "V302" : "0", "heya" : "1", "FL301" : 30}
	globalvars.handshakes = {"FCV301" : "", "V201a" : "", "V201b" :"", "V301" : "", "V302" : "", "heya" : ""}
	print globalvars.timers
	print globalvars.machineState
	print globalvars.handshakes

	ArbiAI = AI.AIclass()

	times = 0

	while True:
		time.sleep(1)
			
		times = times + 1
		if times == 2:
			globalvars.machineState = {"FCV301" : "0", "V201a" : "0", "V201b" :"0", "V301" : "0", "V302" : "0", "heya" : "1", "FL301" : "30"}
			globalvars.handshakes = {"FCV301" : "1", "V201a" : "1", "V201b" :"1", "V301" : "1", "V302" : "1", "heya" : "0"}
		if times == 6:
			globalvars.machineState = {"FCV301" : "1", "V201a" : "1", "V201b" :"1", "V301" : "1", "V302" : "1", "heya" : "1", "FL301" : "30"}
			globalvars.handshakes = {"FCV301" : "1", "V201a" : "1", "V201b" :"1", "V301" : "1", "V302" : "1", "heya" : "1"}
		if times == 9:
			globalvars.machineState = {"FCV301" : "1", "V201a" : "0", "V201b" :"1", "V301" : "0", "V302" : "0", "heya" : "1", "FL301" : "200"}
			globalvars.handshakes = {"FCV301" : "1", "V201a" : "0", "V201b" :"1", "V301" : "1", "V302" : "0", "heya" : "1"} #make handshake wrong
		if times == 10:
			globalvars.machineState = {"FCV301" : "1", "V201a" : "0", "V201b" :"0", "V301" : "0", "V302" : "0", "heya" : "1", "FL301" : "200"}
			globalvars.handshakes = {"FCV301" : "1", "V201a" : "1", "V201b" :"1", "V301" : "1", "V302" : "1", "heya" : "1"}
		if times == 12:
			globalvars.machineState = {"FCV301" : "1", "V201a" : "1", "V201b" :"0", "V301" : "0", "V302" : "0", "heya" : "1", "FL301" : "30"}
			globalvars.handshakes = {"FCV301" : "1", "V201a" : "1", "V201b" :"1", "V301" : "1", "V302" : "1", "heya" : "1"}
		if times == 15:
			globalvars.machineState = {"FCV301" : "1", "V201a" : "1", "V201b" :"0", "V301" : "0", "V302" : "0", "heya" : "1", "FL301" : "10000"}
			globalvars.handshakes = {"FCV301" : "1", "V201a" : "1", "V201b" :"1", "V301" : "0", "V302" : "1", "heya" : ""} # make handshake wrong
		if times == 17:
			globalvars.machineState = {"FCV301" : "1", "V201a" : "0", "V201b" :"0", "V301" : "0", "V302" : "0", "heya" : "1", "FL301" : "10000"}		
			globalvars.handshakes = {"FCV301" : "1", "V201a" : "1", "V201b" :"1", "V301" : "1", "V302" : "1", "heya" : "1"}

		
		outcome = ArbiAI.ArbiCSVFlowReader1.doNextStepInFlowChart()
		print outcome + str(times)
		
		ArbiAI.status()
		ArbiAI.decide()
		
		ArbiAI.ArbiDataLogger.logData(str(globalvars.machineState))
		
		ArbiAI.ArbiUART.serialWrite("1_hi0_ACM0\r\n")
		ArbiAI.ArbiUART.serialWrite("1_hi1_ACM1\r\n")
		ArbiAI.ArbiUART.serialReceive()

		print globalvars.UARTvar
		
		time.sleep(4)

if __name__ == '__main__':
	main()