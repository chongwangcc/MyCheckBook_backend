#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/3/11 16:19 
# @Author : wangchong 
# @Email: chongwangcc@gmail.com
# @File : utils.py 
# @Software: PyCharm
import string
import random

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))