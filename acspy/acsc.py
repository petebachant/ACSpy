# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 14:26:47 2013

@author: Pete Bachant

This program is a wrapper for the ACS C library using ctypes

To-do
-----
A lot of the functions need error handing added, i.e. they don't care what the 
ACSC function returns.
"""

import ctypes
from ctypes import byref
from errors import errors
import numpy as np

acs = ctypes.windll.LoadLibrary('ACSCL_x86.dll')

int32 = ctypes.c_long
uInt32 = ctypes.c_ulong
uInt64 = ctypes.c_ulonglong
double = ctypes.c_double
char = ctypes.c_char
p = ctypes.pointer

# Define motion flags and constants
AMF_WAIT = 0x00000001
AMF_RELATIVE = 0x00000002
AMF_VELOCITY = 0x00000004
AMF_CYCLIC = 0x00000100
AMF_CUBIC = 0x00000400

AST_MOVE = 0x00000020

# Motor states
MST_ENABLE = 0x00000001
MST_INPOS = 0x00000010			
MST_MOVE = 0x00000020
MST_ACC = 0x00000040

SYNCHRONOUS = None
INVALID = -1
IGNORE = -1
ASYNCHRONOUS = -2
NONE = -1
COUNTERCLOCKWISE = 1
CLOCKWISE = -1
INT_BINARY = 4
REAL_BINARY	 = 8
INT_TYPE = 1
REAL_TYPE = 2	

# Dicts for states
mstates = {16 : 'disabled', 17 : 'enabled'}
astates = {97 : 'accelerating', 33 : 'moving', 0 : 'stopped'}


def openCommDirect():
    """Open simulator. Returns communication handle."""
    hcomm = acs.acsc_OpenCommDirect()
    if hcomm == -1:
        error = getLastError()
        if error in errors:
            print "ACS SPiiPlus Error", error+":", errors[error]
        else: print "ACS SPiiPlus Error", error
    return hcomm

def openCommEthernetTCP(address="10.0.0.100", port=701):
    """Address is a string. Port is an int.
    Returns communication handle."""
    hcomm = acs.acsc_OpenCommEthernetTCP(address, port)
    return hcomm

def setVelocity(hcomm, axis, vel, wait=SYNCHRONOUS):
    """Sets axis velocity"""
    acs.acsc_SetVelocity(hcomm, axis, double(vel), wait)

def setAcceleration(hcomm, axis, acc, wait=SYNCHRONOUS):
    """Sets axis acceleration"""
    acs.acsc_SetAcceleration(hcomm, axis, double(acc), wait)
    
def setDeceleration(hcomm, axis, dec, wait=SYNCHRONOUS):
    """Sets axis deceleration"""
    acs.acsc_SetDeceleration(hcomm, axis, double(dec), wait)
    
def setJerk(hcomm, axis, jerk, wait=SYNCHRONOUS):
    acs.acsc_SetAcceleration(hcomm, axis, double(jerk), wait)
    
def getMotorState(hcomm, axis, wait=SYNCHRONOUS):
    """Gets the motor state. Returns 'enabled', 'disabled', 
    or 'something else'."""
    state = ctypes.c_int()
    pstate = ctypes.pointer(state)
    acs.acsc_GetMotorState(hcomm, axis, pstate, wait)
    if state.value in mstates:
        rstate = mstates[state.value]
    else: rstate = 'something else'
    return rstate
    
def getAxisState(hcomm, axis, wait=SYNCHRONOUS):
    """Gets the axis state. Returns 'accelerating', 'moving', 'stopped', or
    'something else'."""
    state = ctypes.c_int()
    pstate = ctypes.pointer(state)
    acs.acsc_GetAxisState(hcomm, axis, pstate, wait)
    if state.value in astates:
        rstate = astates[state.value]
    else: rstate = 'something else'
    return rstate

def registerEmergencyStop():
    """Register the software emergency stop."""
    acs.acsc_RegisterEmergencyStop()

def jog(hcomm, flags, axis, vel, wait=SYNCHRONOUS):
    """Jog move."""
    acs.acsc_Jog(hcomm, flags, axis, double(vel), wait)

def toPoint(hcomm, flags, axis, target, wait=SYNCHRONOUS):
    """Point to point move."""
    acs.acsc_ToPoint(hcomm, flags, axis, double(target), wait)

def toPointM(hcomm, flags, axes, target, wait=SYNCHRONOUS):
    """Initiates a multi-axis move to the specified target. Axes and target
    are entered as tuples. Set flags as None for absolute coordinates."""
    if len(axes) != len(target):
        print "Number of axes and coordinates don't match!"
    else:
        target_array = double*len(axes)
        axes_array = ctypes.c_int*(len(axes) + 1)
        target_c = target_array()
        axes_c = axes_array()
        for n in range(len(axes)):
            target_c[n] = target[n]
            axes_c[n] = axes[n]
        axes_c[-1] = -1
        errorHandling(acs.acsc_ToPointM(hcomm, flags, axes_c, target_c, wait))

def enable(hcomm, axis, wait=SYNCHRONOUS):
    acs.acsc_Enable(hcomm, int32(axis), wait)
    
def disable(hcomm, axis, wait=SYNCHRONOUS):
    acs.acsc_Disable(hcomm, int32(axis), wait)

def getRPosition(hcomm, axis, wait=SYNCHRONOUS):
    pos = double()
    acs.acsc_GetRPosition(hcomm, axis, p(pos), wait)
    return pos.value
    
def getFPosition(hcomm, axis, wait=SYNCHRONOUS):
    pos = double()
    acs.acsc_GetFPosition(hcomm, axis, byref(pos), wait)
    return pos.value
    
def getRVelocity(hcomm, axis, wait=SYNCHRONOUS):
    rvel = double()
    acs.acsc_GetRVelocity(hcomm, axis, byref(rvel), wait)
    return rvel.value
    
def getFVelocity(hcomm, axis, wait=SYNCHRONOUS):
    vel = double()
    acs.acsc_GetFVelocity(hcomm, axis, byref(vel), wait)
    return vel.value
    
def getVelocity(hcomm, axis, wait=SYNCHRONOUS):
    vel = double()
    acs.acsc_GetVelocity(hcomm, axis, byref(vel), wait)
    return pos.value

def closeComm(hcomm):
    """Closes communication with the controller."""
    acs.acsc_CloseComm(hcomm)

def unregisterEmergencyStop():
    acs.acsc_UnregisterEmergencyStop()
    
def getLastError():
    return acs.acsc_GetLastError()
    
def runBuffer(hcomm, buffno, label=None, wait=SYNCHRONOUS):
    """Runs a buffer in the controller."""
    acs.acsc_RunBuffer(hcomm, int32(buffno), label, wait)
    
def stopBuffer(hcomm, buffno, wait=SYNCHRONOUS):
    """Stops a buffer running in the controller."""
    acs.acsc_StopBuffer(hcomm, int32(buffno), wait)
    
def getProgramState(hc, nbuf, wait=SYNCHRONOUS):
    """Returns program state"""
    state = ctypes.c_int()
    acs.acsc_GetProgramState(hc, nbuf, byref(state), wait)
    return state.value
    
def halt(hcomm, axis, wait=SYNCHRONOUS):
    """Halts motion on specified axis."""
    acs.acsc_Halt(hcomm, axis, wait)
    
def declareVariable(hcomm, vartype, varname, wait=SYNCHRONOUS):
    """Declare a variable in the controller."""
    acs.acsc_DeclareVariable(hcomm, vartype, varname, wait)
    
def readInteger(hcomm, buffno, varname, from1=None, to1=None, from2=None, 
                to2=None, wait=SYNCHRONOUS):
    """Reads an integer(s) in the controller."""
    intread = ctypes.c_int()
    acs.acsc_ReadInteger(hcomm, buffno, varname, from1, to1, from2, to2, 
                         p(intread), wait)
    return intread.value

def writeInteger(hcomm, variable, val_to_write, nbuff=NONE, from1=NONE, 
                 to1=NONE, from2=NONE, to2=NONE, wait=SYNCHRONOUS):
    """Writes an integer variable to the controller."""
    val = ctypes.c_int(val_to_write)
    acs.acsc_WriteInteger(hcomm, nbuff, variable, from1, to1,
                 from2, to2, p(val), wait)

def readReal(hcomm, buffno, varname, from1=NONE, to1=NONE, from2=NONE, 
             to2=NONE, wait=SYNCHRONOUS):
    """Read real variable (scalar or array) from the controller."""
    if from2 == NONE and to2 == NONE and from1 != NONE:
        values = np.zeros((to1-from1+1), dtype=np.float64)
        pointer = values.ctypes.data
    elif from2 != NONE:
        values = np.zeros((to1-from1+1, to2-from2+1), dtype=np.float64)
        pointer = values.ctypes.data
    else: 
        values = double()
        pointer = byref(values)
    acs.acsc_ReadReal(hcomm, buffno, varname, from1, to1, from2, to2, 
                      pointer, wait)
    if from1 != NONE:
        return values
    else:
        return values.value
        
def writeReal():
    """Writes a real value to the controller."""
    pass

def uploadDataFromController(hcomm, src, srcname, srcnumformat, from1, to1,
            from2, to2, destfilename, destnumformat, btranspose, wait=0):
    acs.acsc_UploadDataFromController(hcomm, src, srcname, srcnumformat,
            from1, to1, from2, to2, destfilename, destnumformat, 
            btranspose, wait)


def loadBuffer(hcomm, buffnumber, program, count=512, wait=SYNCHRONOUS):
    """Load a buffer into the ACS controller."""
    prgbuff = ctypes.create_string_buffer(str(program), count)
    rv = acs.acsc_LoadBuffer(hcomm, buffnumber, byref(prgbuff), count, wait)
    errorHandling(rv)
    

def loadBuffersFromFile(hcomm, filename, wait=SYNCHRONOUS):
    rv = acs.acsc_LoadBuffersFromFile(hcomm, filename, wait)
    errorHandling(rv)
                                      
                                      
def spline(hcomm, flags, axis, period, wait=SYNCHRONOUS):
    rv = acs.acsc_Spline(hcomm, flags, axis, double(period), wait)
    errorHandling(rv)
    
    
def addPVPoint(hcomm, axis, point, velocity, wait=SYNCHRONOUS):
    acs.acsc_AddPVPoint(hcomm, axis, double(point), double(velocity), wait)
    
    
def addPVTPoint(hcomm, axis, point, velocity, dt, wait=SYNCHRONOUS):
    acs.acsc_AddPVTPoint(hcomm, axis, double(point), double(velocity), 
                         double(dt), wait)
                         
                         
def multiPoint(hcomm, flags, axis, dwell, wait=SYNCHRONOUS):
    acs.acsc_MultiPoint(hcomm, flags, axis, double(dwell), wait)
    
    
def addPoint(hcomm, axis, point, wait=SYNCHRONOUS):
    acs.acsc_AddPoint(hcomm, axis, double(point), wait)
    
    
def extAddPoint(hcomm, axis, point, rate, wait=SYNCHRONOUS):
    acs.acsc_ExtAddPoint(hcomm, axis, double(point), double(rate), wait)
    
    
def endSequence(hcomm, axis, wait=SYNCHRONOUS):
    return acs.acsc_EndSequence(hcomm, axis, wait)
    

def go(hcomm, axis, wait=SYNCHRONOUS):
    acs.acsc_Go(hcomm, axis, wait)

    
def errorHandling(returnvalue):
    if returnvalue == 0:
        error = getLastError()
        if error in errors:
            print "Error", error, errors[error]
        else: print "Error", error
        
def printLastError():
    error = getLastError()
    if error != 0:
        if error in errors:
            print errors[error]
        else:
            print "ACS SPiiPlus Error", error
            
if __name__ == "__main__":
    """Some testing can go here"""
    hc = openCommDirect()
    declareVariable(hc, INT_TYPE, "testvar")
    writeInteger(hc, "testvar", 2)
    print readInteger(hc, NONE, "testvar")
    closeComm(hc)