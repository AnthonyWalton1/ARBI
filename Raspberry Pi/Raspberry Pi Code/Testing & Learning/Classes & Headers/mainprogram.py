#!/usr/bin/env python
import moduletest

print moduletest.ageofqueen
cfcpiano = moduletest.Piano()
cfcpiano.printdetails()

polly = moduletest.Pet("Polly", "Parrot")
print polly.getSpecies()

a = moduletest.timesfour

ans = a(4)
print str(ans)
