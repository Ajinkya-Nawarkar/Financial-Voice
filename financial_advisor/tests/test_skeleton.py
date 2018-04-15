#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from budget_backend.skeleton import fib

__author__ = "Alec West"
__copyright__ = "Alec West"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
