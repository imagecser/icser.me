# coding: utf-8
from math import *

def calc_line(line):
    try:
        return str(eval(line))
    except Exception as e:
        return 'wrong arg'

