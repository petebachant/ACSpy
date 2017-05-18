"""
This is a test for generating an ACSPL+ program
then uploading it to the controller and running it.
"""

from __future__ import division, print_function
from acspy import acsc
import time

#file = open("test/test.prg", "w+")

acs_prg = """
ENABLE 1""" + \
"""
VEL(1) = 1000
PTP/r 1, -900
STOP
"""

#file.write(acs_prg)
#file.close()

print(acs_prg)
hc = acsc.openCommDirect()
acsc.loadBuffer(hc, 0, acs_prg, 512)
acsc.enable(hc, 0)
#acsc.LoadBuffersFromFile(hc, "test/test.prg")
acsc.runBuffer(hc, 0)
time.sleep(1)
print(acsc.getRPosition(hc, 1))
print(acsc.getMotorState(hc, 1))
acsc.closeComm(hc)
