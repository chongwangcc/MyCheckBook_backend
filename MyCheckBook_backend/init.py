#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/3/11 14:49 
# @Author : wangchong 
# @Email: chongwangcc@gmail.com
# @File : init.py 
# @Software: PyCharm
from datetime import datetime
from random import choice
import json

from tools.Entity import *
from tools.SqlTools import *

g_sqlite3_path = "./data/sqlit3.db"
set_db_name(g_sqlite3_path)


def insert_default_user():
    """
    插入默认的用户，只有当表内容为空时，才执行这个
    :return:
    """

    if  UserInfo.is_empty():
        print("insert default user cc, mm")
        userinfo = UserInfo()
        userinfo.user_name = "cc"
        userinfo.password = "123456"
        userinfo.save()

        userinfo = UserInfo()
        userinfo.user_name="mm"
        userinfo.password="123456"
        userinfo.save()


def create_default_checkbook():
    """
    创建默认的记账本
    :return:
    """
    user_cc = fetch_user_info("cc")
    user_mm = fetch_user_info("mm")

    if Checkbook.is_empty():
        checkbook = Checkbook()
        checkbook.checkbook_name = "CM家庭记账本"
        checkbook.create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        checkbook.last_update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        checkbook.description = "家庭记账"
        checkbook.partners = {}
        checkbook.partners["user_id-"+str(user_cc.id)] = "all"
        checkbook.partners["user_id-"+str(user_mm.id)] = "all"
        checkbook.partners = json.dumps(checkbook.partners)
        checkbook.status = "正常"
        checkbook.rules = ""
        checkbook.creator = user_cc.id
        checkbook.accounts={}
        checkbook.accounts["花销账户"]=["生活费", "doodads", "住房基金", "学习基金", "风险备付金"]
        checkbook.accounts["投资账户"] = ["股票账户", "现金账户", "其他"]
        checkbook.accounts["储蓄账户"] = ["现金账户", "应收账款"]
        checkbook.accounts["default"]=["default"]
        checkbook.accounts = json.dumps(checkbook.accounts)
        checkbook.save()


def random_insert_details():
    """
    随机插入几条details，测试统计分析的restful接口用
    :return:
    """
    user_cc = fetch_user_info("cc")
    user_mm = fetch_user_info("mm")
    checkbook = Checkbook.get(checkbook_name="CM家庭记账本")
    for i in range(0, 200):
        print(i)
        t_detailInfo = DetailInfo()
        t_detailInfo.date = choice(["2019-02-28", "2018-02-02", "2019-03-01", "2019-03-15", "2019-02-15"])
        t_detailInfo.month_str = t_detailInfo.date[:7]
        t_detailInfo.money = choice([12, 13, 59, 100, 400])
        t_detailInfo.category = choice(["零食", "社交", "餐饮", "住房", "医疗", "工资"])
        t_detailInfo.remark =choice(["买酸奶", "交话费", "海贼王", "仙剑4", "随便吧", "DMCC"])
        t_detailInfo.isCash = choice(["现金", "信用卡"])
        t_detailInfo.type = choice(["收入", "支出", "流入", "流出"])
        t_detailInfo.account_name = choice(["花销账户", "投资账户", "储蓄账户"])
        t_detailInfo.seconds_account_name = choice(["生活费账户", "doodads账户", "教育账户", "风险备付金", "住房基金"])
        t_detailInfo.updater =  choice([user_cc, user_mm])
        t_detailInfo.checkbook = checkbook
        t_detailInfo.save()



# 插入默认的用户：cc、mm
insert_default_user()
create_default_checkbook()
random_insert_details()
# 创建默认的记账本：CM家庭记账本