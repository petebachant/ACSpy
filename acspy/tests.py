# -*- coding: utf-8 -*-
"""
This module contains tests for the ACSpy package.

"""
from __future__ import division, print_function
from acspy import acsc

def test_write_real():
    print("Testing acsc.writeReal")
    hc = acsc.openCommDirect()
    varname = "SLLIMIT1"
    val = 3.14
    acsc.writeReal(hc, varname, val)
    valread = acsc.readReal(hc, None, varname)
    acsc.closeComm(hc)
    assert(valread == val)
    print("PASS")