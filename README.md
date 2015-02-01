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
The `acsc` module is designed to mimic the syntax of the ACS C library that it wraps. 

```python
>>> from acspy import acsc
>>> hcomm = acsc.openCommDirect()
>>> acsc.enable(hcomm, 0)
>>> acsc.getMotorState(hcomm, 0)
{'moving': False, 'enabled': True, 'in position': True, 'accelerating': False}
>>> acsc.closeComm(hcomm)
```

### Using the `Controller` object
The `control` module provides an object-oriented interface to the controller, making
code development more intuitive. 
An example of its use:

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

License
-------

ACSpy Copyright (c) 2013-2014 Peter Bachant

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
