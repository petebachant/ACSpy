# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 17:16:21 2013

@author: Pete
"""

import win32com.client as wc
import time

acs = wc.Dispatch('SPiiPlusCOM660.Channel.1')

acs.OpenCommDirect()

#acs.RegisterEmergencyStop()

acs.Enable(1)

state = acs.GetAxisState(1)

pos1 = acs.GetRPosition(1)

acs.SetVelocity(1, 1)
acs.SetAcceleration(1, 1)
acs.ToPoint(Flags=0, Axis=1, Point=2)
time.sleep(2)

pos2 = acs.GetRPosition(1)
acs.CloseComm()

#acs.UnregisterEmergencyStop()

