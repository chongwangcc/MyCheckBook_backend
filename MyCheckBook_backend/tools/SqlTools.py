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


def get_Details(checkbook_id, month_str, account_name=None, mtype=None, category=None):
    """
    根据条件获得记账本明细，按照时间排序
    :param checkbook_id:
    :param month_str:
    :param account_name:
    :param mtype:
    :param category:
    :return:
    """
    conn = sqlite3.connect(g_sqlite3_path)
    sql = "select * from " + DetailInfo.get_table_name()
    sql += " where "
    sql += " checkbook == " + str(checkbook_id) + " and "
    sql += " month_str == '" + str(month_str) + "' "
    if account_name is not None:
        account1, account2 = account_name, None
        if "-" in str(account_name):
            account1, account2 = str(account_name).split("-")
        if account1 is not None:
            sql += " and "+" account_name == '" + str(account1) + "' "
        if account2 is not None:
            sql += " and "+" seconds_account_name == '" + str(account2) + "' "
    if mtype is not None:
        sql += " and " + " type == '" + str(mtype) + "' "
    if category is not None:
        sql += " and " + " category == '" + str(category) + "' "

    sql += " ORDER BY date DESC, id ASC "

    df = pd.read_sql_query(sql, conn)
    return df


class UserTools:
    my_user_map = {}

    @classmethod
    def gen_id_to_name(cls, user_id):
        """
        通过user_id获得user名称，
        先查缓存，缓存不存在，在去查数据库
        :param user_id:
        :return:
        """
        user_name = cls.my_user_map.setdefault(user_id,None)
        if user_name is None:
            try:
                user_name = UserInfo.get(id=user_id).user_name
            except:
                pass
        return user_name

if __name__ == "__main__":
    pass
    detias = get_Details(checkbook_id=1, month_str="2019-02")
    print(detias)



