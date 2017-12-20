# coding: utf-8
import random

def image_random(max):
    l_num = random.sample(range(1, max + 1), 32)
    return ["https://img.icser.me/ds/" + str(i) + ".jpg" for i in l_num]

