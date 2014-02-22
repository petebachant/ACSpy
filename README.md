ACSpy
=====

A Python package for working with ACS motion controllers.

Installation
------------
  - `git clone https://github.com/petebachant/ACSpy.git`
  - `python setup.py install`

Usage
-----
### Using the acsc module
The `acsc` module is designed to mimic the syntax of the ACS C library that it wraps. 

```python
>>> from acspy import acsc
>>> hcomm = acsc.openCommDirect()
>>> acsc.enable(hcomm, 0)
>>> acsc.getMotorState(hcomm, 0)
{'moving': False, 'enabled': True, 'in position': True, 'accelerating': False}
>>> acsc.closeComm(hcomm)
```

### Using a Control object
The `control` module contains an object to handle communication with the controller.
This object does not yet implement all of the functions available in the `acsc` module.
An example of its use:

```python
>>> from acspy.control import Control
>>> c = Control("simulator")
>>> c.connect()
>>> c.axisdef(0, "x")
>>> c.enable_axis("x")
>>> c.ptp("x", 10)
>>> c.rpos("x")
10.0
>>> c.disconnect()
```