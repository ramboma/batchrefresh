# -*- coding: utf-8 -*-
import decorator

"""Main module."""

@decorator.timing
def hello():
    print("hello")
hello()