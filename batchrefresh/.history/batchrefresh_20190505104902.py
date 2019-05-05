# -*- coding: utf-8 -*-
import decorator

"""Main module."""

@decorator.timing
def main():
    print("hello")
hello()