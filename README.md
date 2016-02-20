ACSpy
=====

A Python package for working with [ACS motion controllers](https://www.acsmotioncontrol.com/). Note that this project is not 
affiliated with or endorsed by ACS Motion Control. 


Installation
------------

Note that the ACS motion control SPiiPlus User-Mode Driver must be installed and running. Contact ACS to obtain this software.

This Python package can be installed from PyPI via `pip` with

    pip install acspy
    
To install from the source, clone locally and execute

    python setup.py install


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
