ACSpy
=====

A Python package for working with ACS motion controllers.

Usage
-----
The `acsc` module is designed to mimic the syntax of the ACS C library that it wraps. 

```python
>>> from acspy import acsc
>>> hcomm = acsc.openCommDirect()
>>> acsc.enable(hcomm, 0)
>>> acsc.getMotorState(hcomm, 0)
'enabled'
>>> acsc.closeComm(hcomm)
```