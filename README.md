ACSpy
=====

A Python package for working with ACS motion controllers.


Installation
------------
Execute

    pip install acspy


Usage
-----

### Using the `acsc` module

The `acsc` module is designed to mimic the syntax of the ACS C library that it
wraps.

```python
>>> from acspy import acsc
>>> hcomm = acsc.openCommDirect()
>>> acsc.enable(hcomm, 0)
>>> acsc.getMotorState(hcomm, 0)
{'moving': False, 'enabled': True, 'in position': True, 'accelerating': False}
>>> acsc.closeComm(hcomm)
```


### Using the `Controller` object

The `control` module provides an object-oriented interface to the controller,
making code development more intuitive. An example of its use:

```python
>>> from acspy.control import Controller
>>> controller = Controller(contype="simulator", n_axes=4)
>>> controller.connect()
>>> axis0 = controller.axes[0]
>>> axis0.enable()
>>> axis0.enabled
True
>>> axis0.ptp(500.5)
>>> axis0.rpos
500.5
>>> axis0.disable()
>>> controller.disconnect()
```
