# -*- coding: utf-8 -*-
"""
This module contains an [incomplete] object for communicating with an ACS controller.

"""
from acspy import acsc

class Control(object):
    def __init__(self, contype="Simulator"):
        self.contype = contype
        
    def connect(self, address=None):
        if self.contype == "Simulator":
            self.hc = acsc.openCommDirect()
        elif self.contype == "Ethernet":
            self.hc = acsc.openCommEthernetTCP(address="10.0.0.100", port=701)
			
    def enable_axis(self, axis, wait=acsc.SYNCHRONOUS):
        acsc.enable(self.hc, axis, wait)
		
    def disable_axis(self, axis, wait=acsc.SYNCRHONOUS):
        acsc.disable(self.hc, axis, wait)
            
    def ptp(self, axis, target, flags=None, wait=acsc.SYNCHRONOUS):
        acsc.toPoint(self.hc, flags, axis, target, wait)
		
	def disconnect(self):
        acsc.closeComm(self.hc)