#!/usr/bin/env python

# Import headers/modules
import time
import AI
import GlobalVariables
import GlobalFunctions


def main():	
	time.sleep(2)

	HATstarttime = GlobalFunctions.millis()

	GlobalVariables.timers = {"HAT" : HATstarttime}
	GlobalVariables.machineState = {"FCV301" : "0", "V201a" : "0", "V201b" :"0", "V301" : "0", "V302" : "0", "heya" : "1", "FL301" : 30}
	GlobalVariables.handshakes = {"FCV301" : "", "V201a" : "", "V201b" :"", "V301" : "", "V302" : "", "heya" : ""}
	print GlobalVariables.timers
	print GlobalVariables.machineState
	print GlobalVariables.handshakes

	ArbiAI = AI.AIclass("1")

	times = 0

	while True:
		time.sleep(1)
			
		times = times + 1
		if times == 2:
			GlobalVariables.machineState = {"FCV301" : "0", "V201a" : "0", "V201b" :"0", "V301" : "0", "V302" : "0", "heya" : "1", "FL301" : "30"}
			GlobalVariables.handshakes = {"FCV301" : "1", "V201a" : "1", "V201b" :"1", "V301" : "1", "V302" : "1", "heya" : "0"}
		if times == 6:
			GlobalVariables.machineState = {"FCV301" : "1", "V201a" : "1", "V201b" :"1", "V301" : "1", "V302" : "1", "heya" : "1", "FL301" : "30"}
			GlobalVariables.handshakes = {"FCV301" : "1", "V201a" : "1", "V201b" :"1", "V301" : "1", "V302" : "1", "heya" : "1"}
		if times == 9:
			GlobalVariables.machineState = {"FCV301" : "1", "V201a" : "0", "V201b" :"1", "V301" : "0", "V302" : "0", "heya" : "1", "FL301" : "200"}
			GlobalVariables.handshakes = {"FCV301" : "1", "V201a" : "0", "V201b" :"1", "V301" : "1", "V302" : "0", "heya" : "1"} #make handshake wrong
		if times == 10:
			GlobalVariables.machineState = {"FCV301" : "1", "V201a" : "0", "V201b" :"0", "V301" : "0", "V302" : "0", "heya" : "1", "FL301" : "200"}
			GlobalVariables.handshakes = {"FCV301" : "1", "V201a" : "1", "V201b" :"1", "V301" : "1", "V302" : "1", "heya" : "1"}
		if times == 12:
			GlobalVariables.machineState = {"FCV301" : "1", "V201a" : "1", "V201b" :"0", "V301" : "0", "V302" : "0", "heya" : "1", "FL301" : "30"}
			GlobalVariables.handshakes = {"FCV301" : "1", "V201a" : "1", "V201b" :"1", "V301" : "1", "V302" : "1", "heya" : "1"}
		if times == 15:
			GlobalVariables.machineState = {"FCV301" : "1", "V201a" : "1", "V201b" :"0", "V301" : "0", "V302" : "0", "heya" : "1", "FL301" : "10000"}
			GlobalVariables.handshakes = {"FCV301" : "1", "V201a" : "1", "V201b" :"1", "V301" : "0", "V302" : "1", "heya" : ""} # make handshake wrong
		if times == 17:
			GlobalVariables.machineState = {"FCV301" : "1", "V201a" : "0", "V201b" :"0", "V301" : "0", "V302" : "0", "heya" : "1", "FL301" : "10000"}		
			GlobalVariables.handshakes = {"FCV301" : "1", "V201a" : "1", "V201b" :"1", "V301" : "1", "V302" : "1", "heya" : "1"}

		
		outcome = ArbiAI.ArbiCSVFlowReader1.doNextStepInFlowChart()
		print outcome + str(times)
		
		ArbiAI.status()
		ArbiAI.decide()
		
		ArbiAI.ArbiDataLogger.logData(str(GlobalVariables.machineState))
		
		ArbiAI.ArbiUART.serialWrite("1_hi0_ACM0\r\n")
		ArbiAI.ArbiUART.serialWrite("1_hi1_ACM1\r\n")
		ArbiAI.ArbiUART.serialReceive()

		print GlobalVariables.UARTvar
		
		time.sleep(4)

if __name__ == '__main__':
	main()
