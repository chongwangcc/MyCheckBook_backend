#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/29 14:39 
# @Author : wangchong 
# @Email: chongwangcc@gmail.com
# @File : SqlTools.py 
# @Software: PyCharm


from tools.Entity import *
import pandas as pd

g_sqlite3_path = "./data/sqlit3.db"
set_db_name(g_sqlite3_path)


def fetch_user_info(user_name):
    """
    TODO 获得用户信息类
    :param user_name:
    :return:
    """
    try:
        userinfo = User_Info()
        userinfo.user_name = "cc"
        userinfo.password = "123456"
        userinfo.active = 1
        userinfo.auth_token_file = r"./data/.credentials/cc_calendar.json"
        userinfo.calender_server = "google"
        userinfo.calender_name = "时间日志"
        return userinfo
    except:
        pass
    return None


if __name__ == "__main__":
    pass
    print(User_Info.is_user_exist())



