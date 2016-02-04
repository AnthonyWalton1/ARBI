#!/usr/bin/env python

# Import headers/modules
import time
import AIModule
import globalvars
import globalfxns


def main():
	time.sleep(2)
	globalvars.handshakes = {"P101" : "0", "P102" : "0", "P103" : "0"}
	globalvars.machineState = {"P101" : "", "P102" : "", "P103" : ""}

	AI = AIModule.AIClass()
	times = 0
	time.sleep(1)

	while True:
		times = times + 1
		
		globalvars.GlobalComs.serialWrite("2\r\n")
		outcome = AI.EskyController.doNextStepInFlowChart()
		
		#AI.status()
		#AI.decide()
		
		AI.DataLogger.logData(str(globalvars.machineState))
		print "Coms serial receive data:"
		
		globalvars.GlobalComs.serialReceive()
		
		print "End of coms serial receive data"
		print "globalvars.handshakes: " + str(globalvars.handshakes)
		print "globalvars.machineState: " + str(globalvars.machineState)
		
		print outcome + str(times)
		print("\r\n\r\n")
		time.sleep(7)	


if __name__ == '__main__':
	main()
