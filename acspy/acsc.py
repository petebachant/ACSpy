"""This module is a wrapper for the ACS C library using ctypes."""

from __future__ import annotations, division, print_function

import ctypes
import platform
import re
import warnings
from ctypes import byref, create_string_buffer

import numpy as np


class AcscError(Exception):
    pass


# Import the ACS C library DLL
if platform.architecture()[0] == "32bit":
    acs = ctypes.windll.LoadLibrary("ACSCL_x86.dll")
if platform.architecture()[0] == "64bit":
    acs = ctypes.windll.LoadLibrary("ACSCL_x64.dll")

int32 = ctypes.c_long
int64 = ctypes.c_int64
uInt32 = ctypes.c_ulong
uInt64 = ctypes.c_ulonglong
float_ = ctypes.c_float
double = ctypes.c_double
char = ctypes.c_char
p = ctypes.pointer
s = create_string_buffer(256)

# Define motion flags and constants
AMF_WAIT = 0x00000001
AMF_RELATIVE = 0x00000002
AMF_VELOCITY = 0x00000004
AMF_CYCLIC = 0x00000100
AMF_CUBIC = 0x00000400

# Axis states
AST_LEAD = 0x00000001
AST_DC = 0x00000002
AST_PEG = 0x00000004
AST_PEGREADY = 0x00000010
AST_MOVE = 0x00000020
AST_ACC = 0x00000040
AST_SEGMENT = 0x00000080
AST_VELLOCK = 0x00000100
AST_POSLOCK = 0x00000200

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
REAL_BINARY = 8
INT_TYPE = 1
REAL_TYPE = 2
DEFAULT = -1
INFINITE = -1

ax_mflags = {
    "DUMMY": 0,
    "OPEN": 1,
    "MICRO": 2,
    "HOME": 3,
    "STEPPER": 4,
    "ENCLOOP": 5,
    "STEPENC": 6,
    "NANO": 7,
    "BRUSHL": 8,
    "BRUSHOK": 9,
    "PHASE2": 10,
    "DBRAKE": 11,
    "INVENC": 12,
    "INVDOUT": 13,
    "NOTCH": 14,
    "NOFILT": 15,
    "BI_QUAD": 16,
    "DEFCON": 17,
    "FASTSC": 18,
    "ENMOD": 19,
    "DUALLOOP": 20,
    "LINEAR": 21,
    "ABSCOMM": 22,
    "BRAKE": 23,
    "HSSI": 24,
    "GANTRY": 25,
    "BI_QUAD1": 26,
    "HALL": 27,
    "INVHALL": 28,
    "MODULO": 29,
    "USER1": 30,
    "USER2": 31,
}


def open_comm_direct() -> int:
    """Open simulator.

    Returns communication handle.
    """
    warnings.warn(
        "open_comm_direct is deprecated in favor of open_comm_simulator",
        category=DeprecationWarning,
    )
    # Caution: acs does treat errors differently for openComm functions!
    hcomm = acs.acsc_OpenCommDirect()
    if hcomm == -1:
        hcomm = open_comm_simulator()
    if hcomm == -1:
        err = getLastError()
        err_lng = int32()
        s = create_string_buffer(256)
        if (
            acs.acsc_GetErrorString(
                hcomm, int32(err), s, int32(ctypes.sizeof(s)), byref(err_lng)
            )
            != 0
        ):
            s[err_lng.value] = 0
            err_str = s.value.decode("ascii")
            raise AcscError(str(err) + ": " + err_str)
        else:
            raise AcscError(err)
    return hcomm


def openCommDirect() -> int:
    return open_comm_direct()


def open_comm_simulator() -> int:
    # Caution: acs does treat errors differently for openComm functions!
    hcomm = acs.acsc_OpenCommSimulator()
    if hcomm == -1:
        hcomm = open_comm_direct()
    if hcomm == -1:
        err = getLastError()
        err_lng = int32()
        s = create_string_buffer(256)
        if (
            acs.acsc_GetErrorString(
                hcomm, int32(err), s, int32(ctypes.sizeof(s)), byref(err_lng)
            )
            != 0
        ):
            s[err_lng.value] = 0
            err_str = s.value.decode("ascii")
            raise AcscError(str(err) + ": " + err_str)
        else:
            raise AcscError(err)
    return hcomm


def openCommEthernetTCP(address: str = "10.0.0.100", port: int = 701) -> int:
    """Address is a string.

    Returns communication handle."""
    return open_comm_ethernet_tcp(address=address, port=port)


def open_comm_ethernet_tcp(
    address: str = "10.0.0.100", port: int = 701
) -> int:
    hcomm = acs.acsc_OpenCommEthernetTCP(address.encode(), port)
    if hcomm == -1:
        err = getLastError()
        err_lng = int32()
        s = create_string_buffer(256)
        if (
            acs.acsc_GetErrorString(
                hcomm, int32(err), s, int32(ctypes.sizeof(s)), byref(err_lng)
            )
            != 0
        ):
            s[err_lng.value] = 0
            err_str = s.value.decode("ascii")
            raise AcscError(str(err) + ": " + err_str)
        else:
            raise AcscError(err)
    return hcomm


def getSerialNumber(hcomm, wait=SYNCHRONOUS):
    """Retrieves the controller serial number."""
    s = create_string_buffer(256)
    buffer_size = int32(ctypes.sizeof(s))
    ser_num_len = int32()
    call_acsc(
        acs.acsc_GetSerialNumber,
        hcomm,
        s,
        buffer_size,
        byref(ser_num_len),
        wait,
    )
    serial_number = s.value.decode("ascii")
    return serial_number


def get_library_version() -> str:
    resp: int = acs.acsc_GetLibraryVersion()
    # TODO: Turn this into a string by extracting the bits appropriately
    return resp


def setVelocity(hcomm, axis: int, vel: float, wait=SYNCHRONOUS):
    """Sets axis velocity."""
    call_acsc(acs.acsc_SetVelocity, hcomm, axis, double(vel), wait)


def setAcceleration(hcomm, axis: int, acc: float, wait=SYNCHRONOUS):
    """Sets axis acceleration."""
    call_acsc(acs.acsc_SetAcceleration, hcomm, axis, double(acc), wait)


def setDeceleration(hcomm, axis: int, dec: float, wait=SYNCHRONOUS):
    """Sets axis deceleration."""
    call_acsc(acs.acsc_SetDeceleration, hcomm, axis, double(dec), wait)


def setKillDeceleration(hcomm, axis: int, dec: float, wait=SYNCHRONOUS):
    """Sets axis deceleration."""
    call_acsc(acs.acsc_SetKillDeceleration, hcomm, axis, double(dec), wait)


def setJerk(hcomm, axis: int, jerk: float, wait=SYNCHRONOUS):
    """Defines a value of motion jerk."""
    call_acsc(acs.acsc_SetJerk, hcomm, axis, double(jerk), wait)


def setRPosition(hcomm, axis: int, rpos: float, wait=SYNCHRONOUS):
    """Asigns a current value of reference position."""
    call_acsc(acs.acsc_SetRPosition, hcomm, axis, double(rpos), wait)


def getMotorEnabled(hcomm, axis: int, wait=SYNCHRONOUS):
    """Checks if motor is enabled."""
    state = ctypes.c_int()
    call_acsc(acs.acsc_GetMotorState, hcomm, axis, byref(state), wait)
    state = state.value
    return hex(state)[-1] == "1"


def getMotorState(hcomm, axis: int, wait=SYNCHRONOUS):
    """Gets the motor state. Returns a dictionary with the following keys:
    * "enabled"
    * "in position"
    * "moving"
    * "accelerating"
    """
    state = ctypes.c_int()
    call_acsc(acs.acsc_GetMotorState, hcomm, axis, byref(state), wait)
    state = state.value
    mst = {
        "enabled": hex(state)[-1] == "1",
        "in position": hex(state)[-2] == "1",
        "moving": hex(state)[-2] == "2",
        "accelerating": hex(state)[-2] == "4",
    }
    return mst


def getMotorError(hcomm, axis: int, wait=SYNCHRONOUS):
    """Get the motor error for disabling."""
    error = ctypes.c_int()
    call_acsc(acs.acsc_GetMotorError, hcomm, axis, byref(error), wait)
    error = error.value
    return error


def getErrorString(hcomm, error: int):
    """Retrieves the explanation of an error code."""
    err_lng = int32()
    s = create_string_buffer(256)
    call_acsc(
        acs.acsc_GetErrorString,
        hcomm,
        error,
        s,
        int32(ctypes.sizeof(s)),
        byref(err_lng),
    )
    error_string = s.value.decode("ascii")
    return error_string


def getAxisState(hcomm, axis: int, wait=SYNCHRONOUS):
    """Gets the axis state.

    Returns a dictionary with the following keys
        * "lead"
        * "DC"
        * "PEG"
        * "PEGREADY"
        * "moving"
        * "accelerating"
        * "segment"
        * "vel lock"
        * "pos lock"
    """
    state = ctypes.c_int()
    call_acsc(acs.acsc_GetAxisState, hcomm, axis, byref(state), wait)
    state = state.value
    ast = {
        "lead": hex(state)[-1] == "1",
        "DC": hex(state)[-1] == "2",
        "PEG": hex(state)[-1] == "4",
        "PEGREADY": hex(state)[-2] == "1",
        "moving": hex(state)[-2] == "2",
        "accelerating": hex(state)[-2] == "4",
        "segment": hex(state)[-2] == "8",
        "vel lock": hex(state)[-3] == "1",
        "pos lock": hex(state)[-3] == "2",
    }
    return ast


def getFPosition(hcomm, axis: int, wait=SYNCHRONOUS):
    """Retrieves an instant value of the motor feedback position."""
    fposition = ctypes.c_double()
    call_acsc(acs.acsc_GetFPosition, hcomm, axis, byref(fposition), wait)
    fposition = fposition.value
    return fposition


def registerEmergencyStop():
    """Register the software emergency stop."""
    call_acsc(acs.acsc_RegisterEmergencyStop)


def jog(hcomm, flags: int, axis: int, vel: float, wait=SYNCHRONOUS):
    """Initiates a single-axis jog motion."""
    call_acsc(acs.acsc_Jog, hcomm, flags, axis, double(vel), wait)


def toPoint(hcomm, flags: int, axis: int, target: float, wait=SYNCHRONOUS):
    """Point to point move."""
    call_acsc(acs.acsc_ToPoint, hcomm, flags, axis, double(target), wait)


def toPointM(hcomm, flags: int, axes: tuple, target: tuple, wait=SYNCHRONOUS):
    """Initiates a multi-axis move to the specified target. Axes and target
    are entered as tuples. Set flags as None for absolute coordinates."""
    if len(axes) != len(target):
        raise AcscError("Number of axes and coordinates don't match!")
    target_array = double * len(axes)
    axes_array = ctypes.c_int * (len(axes) + 1)
    target_c = target_array()
    axes_c = axes_array()
    for n in range(len(axes)):
        target_c[n] = target[n]
        axes_c[n] = axes[n]
    axes_c[-1] = -1
    call_acsc(acs.acsc_ToPointM, hcomm, flags, axes_c, target_c, wait)


def enable(hcomm, axis: int, wait=SYNCHRONOUS):
    """The function activates a motor."""
    call_acsc(acs.acsc_Enable, hcomm, int32(axis), wait)


def enableMotors(hcomm, axes: list, wait=SYNCHRONOUS):
    """The function activates several motors."""
    axes_array = (ctypes.c_int * len(axes))(*axes)
    call_acsc(acs.acsc_EnableM, hcomm, axes_array, wait)


def commutate(
    hcomm,
    axis,
    current=DEFAULT,
    settle=DEFAULT,
    slope=DEFAULT,
    wait=SYNCHRONOUS,
):
    call_acsc(
        acs.acsc_CommutExt,
        hcomm,
        int32(axis),
        float_(current),
        int32(settle),
        int32(slope),
        wait,
    )


def waitCommutated(hcomm, axis: int, timeout=INFINITE):
    """Wait for commutation to finish.

    Default timeout is 30 seconds.
    """
    call_acsc(
        acs.acsc_WaitMotorCommutated, hcomm, int32(axis), 1, int32(timeout)
    )


def disable(hcomm, axis: int, wait=SYNCHRONOUS):
    """The function shuts off a motor."""
    call_acsc(acs.acsc_Disable, hcomm, int32(axis), wait)


def disableAllMotors(hcomm, wait=SYNCHRONOUS):
    """The function shuts off all motors."""
    call_acsc(acs.acsc_DisableAll, hcomm, wait)


def disableMotors(hcomm, axes: list, wait=SYNCHRONOUS):
    """The function shuts off several specified motors."""
    axes_array = (ctypes.c_int * len(axes))(*axes)
    call_acsc(acs.acsc_DisableM, hcomm, axes_array, wait)


def getRPosition(hcomm, axis: int, wait=SYNCHRONOUS):
    pos = double()
    call_acsc(acs.acsc_GetRPosition, hcomm, axis, p(pos), wait)
    return pos.value


def getFPosition(hcomm, axis: int, wait=SYNCHRONOUS):
    pos = double()
    call_acsc(acs.acsc_GetFPosition, hcomm, axis, byref(pos), wait)
    return pos.value


def getRVelocity(hcomm, axis: int, wait=SYNCHRONOUS):
    rvel = double()
    call_acsc(acs.acsc_GetRVelocity, hcomm, axis, byref(rvel), wait)
    return rvel.value


def getFVelocity(hcomm, axis: int, wait=SYNCHRONOUS):
    vel = double()
    call_acsc(acs.acsc_GetFVelocity, hcomm, axis, byref(vel), wait)
    return vel.value


def getVelocity(hcomm, axis: int, wait=SYNCHRONOUS):
    """Returns current velocity for specified axis."""
    vel = double()
    call_acsc(acs.acsc_GetVelocity, hcomm, axis, byref(vel), wait)
    return vel.value


def getAcceleration(hcomm, axis: int, wait=SYNCHRONOUS):
    """Returns current acceleration for specified axis."""
    val = double()
    call_acsc(acs.acsc_GetAcceleration, hcomm, axis, byref(val), wait)
    return val.value


def getDeceleration(hcomm, axis: int, wait=SYNCHRONOUS):
    """Returns current deceleration for specified axis."""
    val = double()
    call_acsc(acs.acsc_GetDeceleration, hcomm, axis, byref(val), wait)
    return val.value


def getKillDeceleration(hcomm, axis: int, wait=SYNCHRONOUS):
    """Returns current deceleration for specified axis."""
    val = double()
    call_acsc(acs.acsc_GetKillDeceleration, hcomm, axis, byref(val), wait)
    return val.value


def closeComm(hcomm):
    """Closes communication with the controller."""
    call_acsc(acs.acsc_CloseComm, hcomm)


def unregisterEmergencyStop():
    call_acsc(acs.acsc_UnregisterEmergencyStop)


def getLastError():
    return acs.acsc_GetLastError()


def runBuffer(hcomm, buffno, label=None, wait=SYNCHRONOUS):
    """Runs a buffer in the controller."""
    if label is not None:
        label = label.encode()
    call_acsc(acs.acsc_RunBuffer, hcomm, int32(buffno), label, wait)


def stopBuffer(hcomm, buffno, wait=SYNCHRONOUS):
    """Stops a buffer running in the controller."""
    call_acsc(acs.acsc_StopBuffer, hcomm, int32(buffno), wait)


def waitProgramEnd(hcomm, buffno, timeout=INFINITE):
    """Wait for program in buffer buffno to finish"""
    call_acsc(acs.acsc_WaitProgramEnd, hcomm, int32(buffno), int32(timeout))


def getProgramState(hc, nbuf, wait=SYNCHRONOUS):
    """Returns program state"""
    state = ctypes.c_int()
    call_acsc(acs.acsc_GetProgramState, hc, nbuf, byref(state), wait)
    return state.value


def halt(hcomm, axis: int, wait=SYNCHRONOUS):
    """Halts motion on specified axis."""
    call_acsc(acs.acsc_Halt, hcomm, axis, wait)


def declareVariable(hcomm, vartype, varname, wait=SYNCHRONOUS):
    """Declare a variable in the controller."""
    call_acsc(acs.acsc_DeclareVariable, hcomm, vartype, varname.encode(), wait)


def readInteger(
    hcomm,
    buffno,
    varname,
    from1=None,
    to1=None,
    from2=None,
    to2=None,
    wait=SYNCHRONOUS,
):
    """Reads an integer(s) in the controller."""
    intread = ctypes.c_int()
    call_acsc(
        acs.acsc_ReadInteger,
        hcomm,
        buffno,
        varname.encode(),
        from1,
        to1,
        from2,
        to2,
        p(intread),
        wait,
    )
    return intread.value


def writeInteger(
    hcomm,
    variable,
    val_to_write,
    nbuff=NONE,
    from1=NONE,
    to1=NONE,
    from2=NONE,
    to2=NONE,
    wait=SYNCHRONOUS,
):
    """Writes an integer variable to the controller."""
    val = ctypes.c_int(val_to_write)
    call_acsc(
        acs.acsc_WriteInteger,
        hcomm,
        nbuff,
        variable.encode(),
        from1,
        to1,
        from2,
        to2,
        p(val),
        wait,
    )


def readMflag(hcomm, axis: int, flag_nm):
    """read a Mflag. For definition refer to ax_mflags at the top"""
    allFlags = readInteger(hcomm, None, "MFLAGS", axis, axis + 1)
    return bool(((1 << ax_mflags[flag_nm]) & allFlags))


def setMflag(hcomm, axis: int, flag_nm):
    """Set a Mflag. For definition refer to ax_mflags at the top"""
    allFlags = readInteger(hcomm, None, "MFLAGS", axis, axis + 1)
    allFlags |= 2 ** (ax_mflags[flag_nm])
    writeInteger(hcomm, "MFLAGS", allFlags)


def clearMflag(hcomm, axis: int, flag_nm):
    """Clear a Mflag. For definition refer to ax_mflags at the top"""
    allFlags = readInteger(hcomm, None, "MFLAGS", axis, axis + 1)
    allFlags &= ~(2 ** (ax_mflags[flag_nm]))
    writeInteger(hcomm, "MFLAGS", allFlags)


def readReal(
    hcomm,
    buffno,
    varname,
    from1=NONE,
    to1=NONE,
    from2=NONE,
    to2=NONE,
    wait=SYNCHRONOUS,
):
    """Read real variable (scalar or array) from the controller."""
    if from2 == NONE and to2 == NONE and from1 != NONE:
        values = np.zeros((to1 - from1 + 1), dtype=np.float64)
        pointer = values.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    elif from2 != NONE:
        values = np.zeros((to1 - from1 + 1, to2 - from2 + 1), dtype=np.float64)
        pointer = values.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    else:
        values = double()
        pointer = byref(values)
    call_acsc(
        acs.acsc_ReadReal,
        hcomm,
        buffno,
        varname.encode(),
        from1,
        to1,
        from2,
        to2,
        pointer,
        wait,
    )
    if from1 != NONE:
        return values
    else:
        return values.value


def writeReal(
    hcomm,
    varname,
    val_to_write,
    nbuff=NONE,
    from1=NONE,
    to1=NONE,
    from2=NONE,
    to2=NONE,
    wait=SYNCHRONOUS,
):
    """Writes a real value to the controller."""
    val = ctypes.c_double(val_to_write)
    call_acsc(
        acs.acsc_WriteReal,
        hcomm,
        nbuff,
        varname.encode(),
        from1,
        to1,
        from2,
        to2,
        p(val),
        wait,
    )


def uploadDataFromController(
    hcomm,
    src,
    srcname,
    srcnumformat,
    from1,
    to1,
    from2,
    to2,
    destfilename,
    destnumformat,
    btranspose,
    wait=0,
):
    call_acsc(
        acs.acsc_UploadDataFromController,
        hcomm,
        src,
        srcname,
        srcnumformat,
        from1,
        to1,
        from2,
        to2,
        destfilename,
        destnumformat,
        btranspose,
        wait,
    )


def loadBuffer(hcomm, buffnumber, program, count=512, wait=SYNCHRONOUS):
    """Load a buffer into the ACS controller."""
    prgbuff = ctypes.create_string_buffer(str(program).encode(), count)
    call_acsc(
        acs.acsc_LoadBuffer, hcomm, buffnumber, byref(prgbuff), count, wait
    )


def loadBuffersFromFile(hcomm, filename, wait=SYNCHRONOUS):
    # acs.acsc_LoadBuffersFromFile seems to be broken
    # So we mimic it and revert to loadBuffer
    progs = {}
    currbuffer = None
    currprg = ""
    with open(filename) as file:
        rawline = file.readline()
        line = rawline.replace(" ", "").upper()  # strip all spaces, cnv. upper
        if line[:7] == "#HEADER":  # skip the header
            rawline = file.readline()

        while rawline:  # read lines until end of file
            line = rawline.replace(" ", "").upper()
            matchres = re.match("#BUF([0-9]*)", line)  # match #BUF & fol. nums
            if matchres:
                if currbuffer:  # if buffer is not empty
                    progs[currbuffer] = currprg.encode("ascii")
                    currprg = ""
                currbuffer = int(matchres.groups()[0])  # assign buffer
                rawline = file.readline()
            else:
                currprg += rawline
                rawline = file.readline()

    if currbuffer:  # do not forget to add lasf prog
        progs[currbuffer] = currprg

    for key in progs:  # load all buffers
        loadBuffer(hcomm, key, progs[key])


def compileBuffer(hcomm, buffnumber, wait=SYNCHRONOUS):
    call_acsc(acs.acsc_CompileBuffer, hcomm, buffnumber, wait)


def spline(hcomm, flags: int, axis: int, period: float, wait=SYNCHRONOUS):
    call_acsc(acs.acsc_Spline, hcomm, flags, axis, double(period), wait)


def addPVPoint(
    hcomm, axis: int, point: float, velocity: float, wait=SYNCHRONOUS
):
    call_acsc(
        acs.acsc_AddPVPoint, hcomm, axis, double(point), double(velocity), wait
    )


def addPVTPoint(
    hcomm, axis: int, point: float, velocity: float, dt, wait=SYNCHRONOUS
):
    call_acsc(
        acs.acsc_AddPVTPoint,
        hcomm,
        axis,
        double(point),
        double(velocity),
        double(dt),
        wait,
    )


def multiPoint(hcomm, flags: int, axis: int, dwell: float, wait=SYNCHRONOUS):
    call_acsc(acs.acsc_MultiPoint, hcomm, flags, axis, double(dwell), wait)


def addPoint(hcomm, axis: int, point: float, wait=SYNCHRONOUS):
    call_acsc(acs.acsc_AddPoint, hcomm, axis, double(point), wait)


def extAddPoint(hcomm, axis: int, point: float, rate: float, wait=SYNCHRONOUS):
    call_acsc(
        acs.acsc_ExtAddPoint, hcomm, axis, double(point), double(rate), wait
    )


def endSequence(hcomm, axis: int, wait=SYNCHRONOUS):
    call_acsc(acs.acsc_EndSequence, hcomm, axis, wait)


def go(hcomm, axis: int, wait=SYNCHRONOUS):
    call_acsc(acs.acsc_Go, hcomm, axis, wait)


def getOutput(hcomm, port: int, bit: int, wait=SYNCHRONOUS):
    """Returns the value of a digital output."""
    val = int32()
    call_acsc(acs.acsc_GetOutput, hcomm, port, bit, byref(val), wait)
    return val.value


def setOutput(hcomm, port: int, bit: int, val: int, wait=SYNCHRONOUS):
    """Sets the value of a digital output."""
    call_acsc(acs.acsc_SetOutput, hcomm, port, bit, val, wait)


def call_acsc(func, *args, **kwargs):
    """Wraps ACS library to handle errors."""
    rv = func(*args, **kwargs)
    if rv == 0:  # There was an error
        err = acs.acsc_GetLastError()  # Retrieve error code
        err_lng = int32()
        s = create_string_buffer(256)
        hc = args[0]
        if (
            acs.acsc_GetErrorString(
                hc, int32(err), s, int32(ctypes.sizeof(s)), byref(err_lng)
            )
            != 0
        ):
            s[err_lng.value] = b"\x00"
            err_str = s.value.decode("ascii")
            raise AcscError(str(err) + ": " + err_str)
        else:
            raise AcscError(err)
    return rv


def cancelOperation(hcomm, wait=SYNCHRONOUS):
    """Cancels all of the waiting and non-waiting calls."""
    call_acsc(acs.acsc_CancelOperation, hcomm, wait)


if __name__ == "__main__":
    """Some testing can go here"""
    hc = openCommEthernetTCP()
    # hc = openCommDirect()
    print(getOutput(hc, 1, 16))
    closeComm(hc)

    call_acsc(acs.acsc_Halt, hc, 0, SYNCHRONOUS)
