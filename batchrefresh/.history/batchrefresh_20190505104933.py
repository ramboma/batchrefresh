# -*- coding: utf-8 -*-
import decorator

"""Main module."""

@decorator.timing
def main():
    #设置配置对象
    #
    print("hello")
main()