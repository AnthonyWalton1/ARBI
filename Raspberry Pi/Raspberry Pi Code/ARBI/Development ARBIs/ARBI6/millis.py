#!/usr/bin/env python
import time

def millis():
	return int(round(time.time() * 1000))



a = [11]

print all(x == 1 for x in a)
