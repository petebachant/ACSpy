# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 20:36:34 2013

This file calls function from the ACS C library wrapper

@author: Pete
"""

from __future__ import division, print_function
import numpy as np
import matplotlib.pyplot as plt
import acsc
import time


axes = {'y':0, 'z':1, 'turbine':4, 'tow':5}

axis = 5
acc = 1
flags = 0
vel = 1
target = 2

hc = acsc.OpenCommDirect()

if hc == acsc.INVALID:
    print("Cannot connect to controller, error", acsc.GetLastError())

else:    
    acsc.Enable(hc, axis)
    
    time.sleep(0.1)
    
    state = acsc.GetMotorState(hc, axis, acsc.SYNCHRONOUS)
    
    acsc.SetVelocity(hc, axis, vel)
    acsc.SetAcceleration(hc, axis, acc)
    acsc.SetDeceleration(hc, axis, acc)
    
    position = acsc.GetRPosition(hc, axis)
    pvec = [position]
    
    tvec = [time.time()]
    
    acsc.ToPoint(hc, flags, axis, target, acsc.SYNCHRONOUS)
    
    while position != target:
        time.sleep(0.1)
        position = acsc.GetRPosition(hc, axis, acsc.SYNCHRONOUS)
        pvec.append(position)
        tvec.append(time.time())
        
        print("Axis", axis, "is", acsc.GetAxisState(hc, axis))

    
    pvec = np.asarray(pvec)
    tvec = np.asarray(tvec) - tvec[0]
    
    print("Generating plot")
    plt.close('all')
    plt.plot(tvec, pvec)   
    
    acsc.CloseComm(hc)
