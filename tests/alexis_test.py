#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from rca.src.rca.module.calculate_dbz95 import calculate_dbz95_ppi

__author__ = "Alexis Hunzinger"
__copyright__ = "Alexis Hunzinger"
__license__ = "mit"

# Creating a sample function
def a_name(x):
    print('First letter of ',x,' is:', x[0])
    if x[0] == 'A':
        return(1)
    else:
	return(0)

def test_a_name():
    assert a_name('Alexis') == 1
    assert a_name('Brian') == 0
    assert a_name('Apple') == 1
    with pytest.raises(AssertionError):
        a_name('Zenith') == 1
