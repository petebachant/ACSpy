# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 22:31:39 2013

@author: Pete

This module contains an unfinished object for communicating with an ACS controller.
"""

from acsc import acsc

class ACSControl(object):
    def __init__(self, contype="Simulator"):
        self.contype = contype
        self.connect()
        
    def connect(self, address=None):
        if self.contype == "Simulator":
            self.hc = acsc.openCommDirect()
        elif self.contype == "Ethernet":
            self.hc = acsc.openCommEthernetTCP()
            
    def ptp(self, axis, target, flags=None, wait = acsc.SYNCHRONOUS):
        acsc.toPoint(self.hc, flags, axis, target, wait)