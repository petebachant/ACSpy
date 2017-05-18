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
acc = 100
flags = 0
vel = 1
target = 2
dt = 0.01

hc = acsc.OpenCommDirect()

if hc == acsc.INVALID:
    print("Cannot connect to controller, error", acsc.GetLastError())

else:    
    acsc.Enable(hc, axis)
    acsc.SetVelocity(hc, axis, vel)
    acsc.SetAcceleration(hc, axis, acc)
    acsc.SetDeceleration(hc, axis, acc)
    
    pvec = []
    tvec = []
    vvec = []
    
    
    
    t = np.arange(0, 6*np.pi, dt)
    x = np.sin(2*t)
    
    acsc.MultiPoint(hc, None, axis, 0)
        
    for n in range(len(x)):
        acsc.AddPoint(hc, axis, x[n])
    acsc.EndSequence(hc, axis)
    
    while acsc.GetAxisState(hc, axis) != "stopped":
        position = acsc.GetRPosition(hc, axis, acsc.SYNCHRONOUS)
        vel = acsc.GetRVelocity(hc, axis, acsc.SYNCHRONOUS)
        pvec.append(position)
        tvec.append(time.time())
        vvec.append(vel)
        print(position)
        time.sleep(dt*2)
        

    pvec = np.asarray(pvec)
    tvec = np.asarray(tvec) - tvec[0]
    
    print("Generating plot")
    plt.close('all')
    plt.plot(tvec, pvec)   
    plt.hold(True)
    plt.plot(t, x, '--k')

    
    acsc.CloseComm(hc)
