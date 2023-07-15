"""Read a real value from a controller."""

from __future__ import division, print_function

from acspy import acsc

hc = acsc.openCommDirect()

print(acsc.readReal(hc, acsc.NONE, "FPOS(0)"))

acsc.closeComm(hc)
