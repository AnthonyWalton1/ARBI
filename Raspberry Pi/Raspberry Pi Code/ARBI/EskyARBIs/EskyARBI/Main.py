#!/usr/bin/env python

# Import headers/modules
import time
import AIModule
import globalvars
import globalfxns


def main():
	time.sleep(2)
	globalvars.handshakes = {"P101" : "1", "P102" : "1", "P103" : "1"}

	AI = AIModule.AIClass()
	times = 0
	time.sleep(1)

	while True:
		times = times + 1
		print globalvars.timers
				
		outcome = AI.EskyController.doNextStepInFlowChart()
		print outcome + str(times)
		
		AI.status()
		AI.decide()
		
		AI.DataLogger.logData(str(globalvars.machineState))
		
		AI.Coms.serialWrite("1_hi0_ACM0\r\n")
		AI.Coms.serialWrite("1_hi1_ACM1\r\n")
		AI.Coms.serialReceive()
		
		print globalvars.ComsVar
		
		time.sleep(38)

if __name__ == '__main__':
	main()
