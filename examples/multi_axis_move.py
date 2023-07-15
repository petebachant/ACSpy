# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 22:45:36 2013

This is a multi axis move.

@author: Pete
"""

from acsc import acsc
import time

hc = acsc.openCommDirect()

acsc.enable(hc, 0)
acsc.enable(hc, 1)

acsc.toPointM(hc, None, (0,1), (1,2))

time.sleep(1)

pos0 = acsc.getRPosition(hc, 0)
pos1 = acsc.getRPosition(hc,1)

acsc.closeComm(hc)