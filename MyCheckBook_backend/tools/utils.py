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


def get_now_str():
    """
    获得当前时间字符串，精确到秒
    :return:
    """
    from datetime import datetime
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return now_str


class AssetsSumUtils():
    """
    计算Assets 汇总信息的类
    """
    def __init__(self):
        self.all_result = {}
        self.sumName = "合并账户"

    def add(self, org_price, now_price, appendix_name, fluidity, account_name):
        """
        添加一条记录
        :param org_price:
        :param now_price:
        :param appendix_name:
        :param fluidity:
        :param account_name:
        :return:
        """

    def get_final_result(self):
        return self.all_result


