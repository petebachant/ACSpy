# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 23:26:33 2013

@author: Pete
"""

from __future__ import division, print_function
from acspy import acsc

hc = acsc.openCommDirect()

print(acsc.readReal(hc, acsc.NONE, "FPOS(0)"))

acsc.closeComm(hc)
