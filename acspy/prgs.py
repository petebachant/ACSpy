"""Functionality for generating ACSPL+ programs."""

from __future__ import division, print_function


class ACSPLplusPrg(object):
    def __init__(self):
        self.txt = ""

    def declare_array(self, scope, arraytype, name, length):
        """Declares an array."""
        self.txt += scope + " " + arraytype + " " + name
        self.txt += "(" + str(length) + ")\n"

    def declare_2darray(self, scope, arraytype, name, rows, cols):
        """Declares a 2D array."""
        self.txt += scope + " " + arraytype + " " + name
        self.txt += "(" + str(rows) + ")(" + str(cols) + ")\n"

    def addline(self, linestring):
        self.txt += linestring + "\n"

    def addptp(self, axis, target, switch="", vel=None):
        """Adds a point to point move to the program."""
        self.txt += "PTP" + switch + " " + str(axis) + ", " + str(target)
        self.txt += "\n"

    def add_dc(self, array_name, length, sr, varname, switch=""):
        """Adds a data collection line to the program."""
        self.txt += "DC" + switch + " " + array_name + ", " + str(length)
        self.txt += ", " + str(1 / sr * 1000) + ", " + varname + "\n"

    def addstopline(self):
        self.txt += "STOP"

    def save(self, filename):
        pass

    def __str__(self):
        return self.txt
