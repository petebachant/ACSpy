# -*- coding: utf-8 -*-
"""
This module contains an [incomplete] object for communicating with an ACS controller.

"""
from acspy import acsc


class Control(object):
    def __init__(self, contype="simulator"):
        self.contype = contype
        self.axisdefs = {}
        
    def connect(self, address=None):
        if self.contype == "simulator":
            self.hc = acsc.openCommDirect()
        elif self.contype == "ethernet":
            self.hc = acsc.openCommEthernetTCP(address="10.0.0.100", port=701)
	
    def enable_axis(self, axis, wait=acsc.SYNCHRONOUS):
        if axis in self.axisdefs:
            axis = self.axisdefs[axis]
        acsc.enable(self.hc, axis, wait)

    def disable_axis(self, axis, wait=acsc.SYNCHRONOUS):
        if axis in self.axisdefs:
            axis = self.axisdefs[axis]
        acsc.disable(self.hc, axis, wait)
            
    def ptp(self, axis, target, flags=None, wait=acsc.SYNCHRONOUS):
        if axis in self.axisdefs:
            axis = self.axisdefs[axis]
        acsc.toPoint(self.hc, flags, axis, target, wait)
        
    def rpos(self, axis):
        if axis in self.axisdefs:
            axis = self.axisdefs[axis]
        return acsc.getRPosition(self.hc, axis)
        
    def axisdef(self, axis, axisname):
        """Defines an alias to an axis."""
        self.axisdefs[axisname] = axis
        
    def disconnect(self):
        acsc.closeComm(self.hc)
        

if __name__ == "__main__":
    import time
    c = Control()
    c.connect()
    c.axisdef(0, "x")
    c.enable_axis("x")
    c.ptp("x", 10)
    time.sleep(0.1)
    print c.rpos("x")
    c.disconnect()