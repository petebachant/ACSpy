# -*- coding: utf-8 -*-
"""
This module contains tests for the ACSpy package.
"""
from __future__ import division, print_function
from acspy import acsc, control
import time


def test_write_real():
    print("Testing acsc.writeReal")
    hc = acsc.openCommDirect()
    varname = "SLLIMIT1"
    val = 3.14
    acsc.writeReal(hc, varname, val)
    valread = acsc.readReal(hc, None, varname)
    acsc.closeComm(hc)
    print("Input value:", val)
    print("Value read:", valread)
    assert valread == val
    print("PASS")


def test_controller():
    """Tests the Controller object."""
    print("Testing the Controller object")
    controller = control.Controller("simulator")
    controller.connect()
    x = controller.axes[0]
    assert(x.rpos==0)
    x.enable()
    x.vel = 10000
    x.acc = 100000
    x.dec = 100000
    x.ptp(1000)
    time.sleep(1)
    assert(x.rpos==1000)
    assert(x.acc==100000)
    assert(x.dec==100000)
    controller.disconnect()
    print("PASS")


def test_upload_prg():
    """Test that a program can be uploaded and run in the simulator."""
    hc = acsc.openCommDirect()
    txt = "VEL(0) = 1.33\nSTOP"
    acsc.loadBuffer(hc, 19, txt, 512)
    acsc.runBuffer(hc, 19)
    vel = acsc.getVelocity(hc, 0)
    print("Velocity:", vel)
    assert vel == 1.33
    acsc.closeComm(hc)
