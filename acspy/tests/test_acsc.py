"""Tests for ``acspy.acsc``."""

from acspy import acsc


def test_open_comm_simulator():
    hc = acsc.open_comm_simulator()
    assert hc != -1


def test_open_comm_direct():
    hc = acsc.open_comm_direct()
    assert hc != -1
