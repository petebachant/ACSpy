"""Tests for the ACSpy package."""

from __future__ import division, print_function

import time

import numpy as np

from acspy import acsc, control, prgs


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
    """Test the Controller object."""
    print("Testing the Controller object")
    controller = control.Controller("simulator")
    controller.connect()
    x = controller.axes[0]
    assert x.rpos == 0
    x.enable()
    x.vel = 10000
    x.acc = 100000
    x.dec = 100000
    x.ptp(1000)
    time.sleep(1)
    assert x.rpos == 1000
    assert x.acc == 100000
    assert x.dec == 100000
    controller.disconnect()
    print("PASS")


def test_upload_prg():
    """Test that a program can be uploaded and run in the simulator."""
    hc = acsc.openCommDirect()
    txt = "enable 0\nVEL(0) = 1333\nptp 0, 1.33\nSTOP"
    acsc.loadBuffer(hc, 19, txt, 64)
    acsc.runBuffer(hc, 19)
    time.sleep(0.2)
    vel = acsc.getVelocity(hc, 0)
    pos = acsc.getRPosition(hc, 0)
    print("Position:", pos)
    print("Velocity:", vel)
    assert vel == 1333.0
    assert pos == 1.33
    acsc.closeComm(hc)


def test_data_collection():
    """Test continuous data collection."""
    hc = acsc.openCommDirect()
    collectdata = True
    data = {
        "carriage_vel": np.array([]),
        "turbine_rpm": np.array([]),
        "time": np.array([]),
    }
    dblen = 100
    sr = 1000
    sleeptime = float(dblen) / float(sr) / 2 * 1.05
    print("Sleep time (s):", sleeptime)
    # Create a data collection program
    prg = prgs.ACSPLplusPrg()
    prg.declare_2darray("GLOBAL", "real", "data", 3, dblen)
    prg.addline("GLOBAL REAL start_time")
    prg.addline("GLOBAL INT collect_data")
    prg.addline("collect_data = 1")
    prg.add_dc("data", dblen, sr, "TIME, FVEL(5), FVEL(4)", "/c")
    prg.addline("start_time = TIME")
    prg.addline("TILL collect_data = 0")
    prg.addline("STOPDC")
    prg.addstopline()
    print("Program:\n", prg)
    # Load program into the a buffer
    acsc.loadBuffer(hc, 19, prg, 1024)
    acsc.runBuffer(hc, 19)
    collect = acsc.readInteger(hc, acsc.NONE, "collect_data")
    while collect == 0:
        time.sleep(0.01)
        collect = acsc.readInteger(hc, acsc.NONE, "collect_data")
    for n in range(10):
        print("Data collection iteration", n)
        time.sleep(sleeptime)
        t0 = acsc.readReal(hc, acsc.NONE, "start_time")
        print("Start time:", t0)
        to2 = dblen // 2 - 1
        print("to2:", to2)
        newdata = acsc.readReal(
            hcomm=hc,
            buffno=acsc.NONE,
            varname="data",
            from1=0,
            to1=2,
            from2=0,
            to2=to2,
        )
        t = (newdata[0] - t0) / 1000.0
        data["time"] = np.append(data["time"], t)
        data["carriage_vel"] = np.append(data["carriage_vel"], newdata[1])
        data["turbine_rpm"] = np.append(data["turbine_rpm"], newdata[2])
        time.sleep(sleeptime)
        from2 = dblen // 2
        to2 = dblen - 1
        print(f"from2: {from2} -- to2: {to2}")
        newdata = acsc.readReal(
            hcomm=hc,
            buffno=acsc.NONE,
            varname="data",
            from1=0,
            to1=2,
            from2=from2,
            to2=to2,
        )
        t = (newdata[0] - t0) / 1000.0
        data["time"] = np.append(data["time"], t)
        data["time"] = data["time"] - data["time"][0]
        data["carriage_vel"] = np.append(data["carriage_vel"], newdata[1])
        data["turbine_rpm"] = np.append(data["turbine_rpm"], newdata[2])
        print(data)


def test_acsplplusprg():
    prg = prgs.ACSPLplusPrg()
    prg.addline("test")
    prg.addstopline()
    print(prg)
