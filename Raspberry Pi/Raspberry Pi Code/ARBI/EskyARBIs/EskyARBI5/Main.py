#!/usr/bin/env python

# Import headers/modules
import time
import AIModule
import globalvars
import globalfxns


def main():
	time.sleep(5)
	globalvars.handshakes = {"P101" : "0", "P102" : "0", "P103" : "0"}
	globalvars.machineState = {"P101" : "", "P102" : "", "P103" : ""}

	AI = AIModule.AIClass()
	times = 0
	time.sleep(1)

	while True:
		times = times + 1
		
		globalvars.GlobalComs.serialWrite("2\r\n")
		time.sleep(0.5)
		outcome = AI.EskyController.doNextStepInFlowChart()
		
		#AI.status()
		#AI.decide()
		
		AI.DataLogger.logData(str(globalvars.machineState))
		print "Coms serial receive data:"
		time.sleep(0.5)
		globalvars.GlobalComs.serialReceive()
		
		print "End of coms serial receive data"
		print "globalvars.handshakes at end of current step after receive updating: " + str(globalvars.handshakes)
		print "globalvars.machineState at end of current step after receive updating: " + str(globalvars.machineState)
		
		print outcome + str(times)
		print("\r\n\r\n")
		time.sleep(0.5)	


if __name__ == '__main__':
	main()
