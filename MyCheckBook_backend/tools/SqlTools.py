#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/29 14:39 
# @Author : wangchong 
# @Email: chongwangcc@gmail.com
# @File : SqlTools.py 
# @Software: PyCharm

import pandas as pd
import json

from tools.Entity import *

g_sqlite3_path = "./data/sqlit3.db"
set_db_name(g_sqlite3_path)


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

    @classmethod
    def fetch_user_info(cls, user_name):
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


class CheckbookTools:
    """
    记账本操作的工具类
    """

    @classmethod
    def fetch_all_checkbooks(cls, user_id):
        """
        根据用户id，获得所有的记账本
        :param cls:
        :param user_id:
        :return:
        """
        try:
            checkbooks = Checkbook.gets(operator="like", partners="%user_id-" + str(user_id) + "%")
            return checkbooks
        except:
            pass
        return []

    @classmethod
    def get_checkbook_full(cls, checkbook_id):
        """
        获得一条记账本的详情
        :param checkbook_id:
        :return: 字典
        """
        checkbook = Checkbook.get(id=checkbook_id)

        t_check = {}
        t_check["checkbook_id"] = checkbook.id
        t_check["checkbook_name"] = checkbook.checkbook_name
        t_check["create_time"] = checkbook.create_time
        t_check["last_update_time"] = checkbook.last_update_time
        t_check["description"] = checkbook.description
        t_check["status"] = checkbook.status
        t_check["partner"] = []
        user_ids = json.loads(checkbook.partners)
        for user_id, permission in user_ids.items():
            t_user = UserInfo.get(id=user_id.replace("user_id-", ""))
            t_check["partner"].append(t_user.user_name)
        t_check["creator"] = UserInfo.get(id=checkbook.creator).user_name
        account_id_list = checkbook.account_id_list
        t_check["accounts"] = {}
        if account_id_list is not None and len(account_id_list)>0:
            t_account_id_list = json.loads(account_id_list)
            for t_account_id in t_account_id_list:
                account_t = AccountInfo.get(id=t_account_id)
                if len(account_t.supportType)>0:
                    t_check["accounts"][account_t.fullname] = json.loads(account_t.supportType)

        # 类别
        t_check["category"] = {}
        categorys = CategoryInfo.gets(checkbook_id=checkbook_id)
        for cate in categorys:
            ll = t_check["category"].setdefault(cate.type,[])
            ll.append(cate.name)

        return t_check


class DetailTools:
    """
    明细操作
    """

    @classmethod
    def create_detail(cls, detial_dict):
        """
        创建一条新的明细记录
        :param detial_dict:
        :return:
        """
        # TODO 0.检查参数格式是否正确

        # 1. 构造detail
        t_detail = DetailInfo()
        t_detail.date = detial_dict["date"]
        t_detail.month_str = t_detail.date[:7]
        t_detail.money = detial_dict["money"]
        t_detail.category = detial_dict["category"]
        t_detail.remark = detial_dict["remark"]
        t_detail.updater = UserTools.fetch_user_info(detial_dict["updater"]).id
        t_detail.checkbook = int(detial_dict["checkbook_id"])
        t_detail.type = detial_dict["type"]
        t_detail.isCash = detial_dict["isCash"]
        if "-" not in detial_dict["account_name"] :
            account_name = detial_dict["account_name"]
            seconds_account_name=""
        else:
            account_name,seconds_account_name = detial_dict["account_name"].split("-")
        t_detail.account_name = account_name
        t_detail.seconds_account_name = seconds_account_name

        # 2.保存
        dd = t_detail.save()
        return dd


if __name__ == "__main__":
    pass
    detias = get_Details(checkbook_id=1, month_str="2019-02")
    print(detias)



