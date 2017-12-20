# coding: utf-8
import random

def image_random(maxv):
    l_num = random.sample(range(1, maxv + 1), 32)
    l_num = [str(i) for i in l_num]
    return l_num

