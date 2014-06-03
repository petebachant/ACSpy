# -*- coding: utf-8 -*-
"""
This module contains an [incomplete] object for communicating with an ACS controller.

"""
from __future__ import division, print_function
from acspy import acsc

class Controller(object):
    def __init__(self, contype="simulator"):
        self.contype = contype
        self.axisdefs = {}
        
    def connect(self, address="10.0.0.100", port=701):
        if self.contype == "simulator":
            self.hc = acsc.openCommDirect()
        elif self.contype == "ethernet":
            self.hc = acsc.openCommEthernetTCP(address=address, port=port)
	
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
        

class Axis(object):
    def __init__(self, controller, axisno, name=None):
        if isinstance(controller, Controller):
            self.controller = controller
        else:
            raise TypeError("Controller is not a valid Controller object")
        self.axisno = axisno
        
    def enable(self, wait=acsc.SYNCHRONOUS):
        acsc.enable(self.controller.hc, self.axisno, wait)
        
    def ptp(self, target, coordinates="absolute", wait=acsc.SYNCHRONOUS):
        """Performs a point to point move in either relative or absolute
        (default) coordinates."""
        if coordinates == "relative":
            flags = acsc.AMF_RELATIVE
        else:
            flags = None
        acsc.toPoint(self.controller.hc, flags, self.axisno, target, wait)
        
    def ptpr(self, distance, wait=acsc.SYNCHRONOUS):
        """Performance a point to point move in relative coordinates."""
        self.ptp(distance, coordinates="absolute", wait=wait)
        
    @property
    def axis_state(self):
        """Returns axis state dict."""
        return acsc.getAxisState(self.controller.hc, self.axisno)
        
    @property
    def motor_state(self):
        """Returns motor state dict."""
        return acsc.getMotorState(self.controller.hc, self.axisno)
        
    @property
    def moving(self):
        return self.motor_state["moving"]
        
    @property
    def enabled(self):
        return self.motor_state["enabled"]
        
    @property
    def in_position(self):
        return self.motor_state["in position"]
        
    @property
    def accelerating(self):
        return self.motor_state["accelerating"]
        
    @property
    def rpos(self):
        return acsc.getRPosition(self.controller.hc, self.axisno)

    @property
    def fpos(self):
        return acsc.getFPosition(self.controller.hc, self.axisno)
        
    @property
    def rvel(self):
        return acsc.getRVelocity(self.controller.hc, self.axisno)

    @property
    def fvel(self):
        return acsc.getFVelocity(self.controller.hc, self.axisno)
        
    @property
    def vel(self):
        return acsc.getVelocity(self.controller.hc, self.axisno)
    @vel.setter
    def vel(self, velocity):
        """Sets axis velocity."""
        acsc.setVelocity(self.controller.hc, self.axisno, velocity)
        
    @property
    def acc(self):
        return acsc.getAcceleration(self.controller.hc, self.axisno)
    @acc.setter
    def acc(self, accel):
        """Sets axis velocity."""
        acsc.setAcceleration(self.controller.hc, self.axisno, accel)
        
    @property
    def dec(self):
        return acsc.getDeceleration(self.controller.hc, self.axisno)
    @dec.setter
    def dec(self, decel):
        """Sets axis velocity."""
        acsc.setDeceleration(self.controller.hc, self.axisno, decel)
        

if __name__ == "__main__":
    import time
    
    controller = Controller("simulator")
    controller.connect()
    
    axis0 = Axis(controller, 0)

    print(axis0.rpos)

    axis0.enable()
    
    axis0.vel = 1000
    axis0.acc = 100000
    axis0.dec = 100000
    
    axis0.ptp(100000)
    time.sleep(1)
    print(axis0.rpos)
    print(axis0.acc)
    print(axis0.dec)
    
    controller.disconnect()
    