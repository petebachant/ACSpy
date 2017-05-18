# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 21:46:10 2013

@author: Pete

This example shows how to collect data from the ACS controller

The 2D arrays are arranged as one variable per row

It's a good idea to keep the data buffer length dblen at least half the
sample rate sr. 

"""

from __future__ import division, print_function
from acspy import acsc, prgs
import numpy as np
import time
import matplotlib.pyplot as plt


plt.close("all")

dblen = 100
sr = 200.0
sleeptime = dblen/sr/2*1.05

t = np.array([])
data = np.array([])

# Connect to controller
hc = acsc.openCommDirect()

# Create an ACSPL+ program to load into the controller
prg = prgs.ACSPLplusPrg()
prg.declare_2darray("global", "real", "data", 2, dblen)
prg.addline("global real foo")
prg.addline("foo = 6.5")
prg.addline("ENABLE 0")
prg.add_dc("data", dblen, sr, "TIME, FVEL(0)", "/c")
for n in range(3):
    prg.addptp(0, 10000, "/e")
    prg.addptp(0, 0, "/e")
prg.addline("WAIT 10000")
prg.addline("STOPDC")
prg.addstopline()

acsc.setAcceleration(hc, 0, 10000)
acsc.loadBuffer(hc, 0, prg, 1024)
acsc.runBuffer(hc, 0)

astate = acsc.getAxisState(hc, 0)
#print astate

for n in range(3):
    time.sleep(sleeptime)
    newdata = acsc.readReal(hc, acsc.NONE, "data", 0, 1, 0, dblen/2-1)
    print(acsc.readInteger(hc, acsc.NONE, "S_DCN"))
    t = np.append(t, newdata[0])
    data = np.append(data, newdata[1])
    time.sleep(sleeptime)
    newdata = acsc.readReal(hc, acsc.NONE, "data", 0, 1, dblen/2, dblen-1)
    t = np.append(t, newdata[0])
    data = np.append(data, newdata[1])

print(acsc.readReal(hc, acsc.NONE, "foo"))
acsc.printLastError()
acsc.closeComm(hc)

plt.plot(t, data)
plt.show()
