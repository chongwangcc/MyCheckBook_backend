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
    获得用户信息
    :param user_name:
    :return:
    """
    try:
        userinfo = UserInfo.get(user_name=user_name)
        return userinfo
    except:
        pass
    return None


def fetch_all_checkbooks(user_id):
    """
    根据用户id，获得所有的记账本
    :param user_id:
    :return:
    """
    try:
        checkbooks = Checkbook.gets(operator="like", partners="%user_id-"+str(user_id)+"%")
        return checkbooks
    except:
        pass
    return []

if __name__ == "__main__":
    pass
    checkbooks = fetch_all_checkbooks(user_id=1)
    print(checkbooks)



