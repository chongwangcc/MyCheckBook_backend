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
    user_cc = UserTools.fetch_user_info("cc")
    user_mm = UserTools.fetch_user_info("mm")

    # 创建记账本
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
        checkbook.creator = user_cc.id
        checkbook.account_id_list = ""
        checkbook.save()

        # 创建 几条默认账户 结构

        all_support = {
            "收入": ["现金", "信用卡"],
            "支出": ["现金", "信用卡"],
            "流入": ["现金"],
            "流出": ["现金"],
        }



        checkbook = Checkbook.get(checkbook_name="CM家庭记账本")
        account_1 = AccountInfo()
        account_1.name = "花销账户"
        account_1.fullname = "花销账户"
        account_1.parent_acccount = 0
        account_1.children_account = ""
        account_1.supportType= ""
        account_1.isGenRport = True
        account_1.description = ""
        account_1.belong_checkbook = checkbook
        account_1.save()

        account_2 = AccountInfo()
        account_2.name = "投资账户"
        account_2.fullname = "投资账户"
        account_2.parent_acccount = 0
        account_2.children_account = ""
        account_2.supportType=""
        account_2.isGenRport = True
        account_2.description = ""
        account_2.belong_checkbook = checkbook
        account_2.save()

        account_3 = AccountInfo()
        account_3.name = "储蓄账户"
        account_3.fullname = "储蓄账户"
        account_3.parent_acccount = 0
        account_3.children_account = ""
        account_3.supportType=json.dumps(all_support)
        account_3.isGenRport = True
        account_3.description = ""
        account_3.belong_checkbook = checkbook
        account_3.save()


        account_1 = AccountInfo()
        account_1.name = "default"
        account_1.fullname = "default"
        account_1.parent_acccount = 0
        account_1.children_account = ""
        account_1.supportType=json.dumps(all_support)
        account_1.isGenRport = True
        account_1.description = ""
        account_1.belong_checkbook = checkbook
        account_1.save()


        account_1 = AccountInfo()
        account_1.name = "生活费账户"
        account_1.fullname = "花销账户-生活费账户"
        account_1.parent_acccount = 1
        account_1.children_account = ""
        account_1.supportType=json.dumps(all_support)
        account_1.isGenRport = False
        account_1.description = ""
        account_1.belong_checkbook = checkbook
        account_1.save()

        account_1 = AccountInfo()
        account_1.name = "doodads账户"
        account_1.fullname = "花销账户-doodads账户"
        account_1.parent_acccount = 1
        account_1.children_account = ""
        account_1.supportType=json.dumps(all_support)
        account_1.isGenRport = False
        account_1.description = ""
        account_1.belong_checkbook = checkbook
        account_1.save()

        account_1 = AccountInfo()
        account_1.name = "教育基金"
        account_1.fullname = "花销账户-教育基金"
        account_1.parent_acccount = 1
        account_1.children_account = ""
        account_1.supportType=json.dumps(all_support)
        account_1.isGenRport = False
        account_1.description = ""
        account_1.belong_checkbook = checkbook
        account_1.save()

        account_1 = AccountInfo()
        account_1.name = "住房账户"
        account_1.fullname = "花销账户-住房账户"
        account_1.parent_acccount = 1
        account_1.children_account = ""
        account_1.supportType=json.dumps(all_support)
        account_1.isGenRport = False
        account_1.description = ""
        account_1.belong_checkbook = checkbook
        account_1.save()

        account_1 = AccountInfo()
        account_1.name = "风险备付金"
        account_1.fullname = "花销账户-风险备付金"
        account_1.parent_acccount = 1
        account_1.children_account = ""
        account_1.supportType=json.dumps(all_support)
        account_1.isGenRport = False
        account_1.description = ""
        account_1.belong_checkbook = checkbook
        account_1.save()

        account_1 = AccountInfo()
        account_1.name = "股票资金"
        account_1.fullname = "投资账户-股票资金"
        account_1.parent_acccount = 2
        account_1.children_account = ""
        account_1.supportType=json.dumps(all_support)
        account_1.isGenRport = False
        account_1.description = ""
        account_1.belong_checkbook = checkbook
        account_1.save()

        account_1 = AccountInfo()
        account_1.name = "现金账户"
        account_1.fullname = "投资账户-现金账户"
        account_1.parent_acccount = 2
        account_1.children_account = ""
        account_1.supportType=json.dumps(all_support)
        account_1.isGenRport = False
        account_1.description = ""
        account_1.belong_checkbook = checkbook
        account_1.save()

        checkbook.account_id_list = json.dumps([i for i in range(1,12)])
        checkbook.save()


def random_insert_details():
    """
    随机插入几条details，测试统计分析的restful接口用
    :return:
    """
    user_cc = UserTools.fetch_user_info("cc")
    user_mm = UserTools.fetch_user_info("mm")
    checkbook = Checkbook.get(checkbook_name="CM家庭记账本")
    for i in range(0, 200):
        print(i)
        t_detailInfo = DetailInfo()
        t_detailInfo.date = choice(["2019-02-28", "2018-02-02", "2019-03-01", "2019-03-15", "2019-02-15"])
        t_detailInfo.month_str = t_detailInfo.date[:7]
        t_detailInfo.money = choice([12, 13, 59, 100, 400])
        t_detailInfo.category = choice(["零食", "社交", "餐饮", "住房", "医疗", "工资"])
        t_detailInfo.remark =choice(["买酸奶", "交话费", "海贼王", "仙剑4", "随便吧", "DMCC"])
        t_detailInfo.updater =  choice([user_cc, user_mm])
        t_detailInfo.checkbook = checkbook
        # 随机选择一个账户
        account_t = None
        while account_t is None:
            account_id = choice(json.loads(checkbook.account_id_list))
            account_t = AccountInfo.get(id=account_id)
            if account_t.supportType is None or len(account_t.supportType)<=0:
                account_t = None

        supportType = json.loads(account_t.supportType)

        t_detailInfo.type = choice(list(supportType.keys()))
        t_detailInfo.isCash = choice(supportType[t_detailInfo.type])

        if "-" not in account_t.fullname :
            account_name = account_t.fullname
            seconds_account_name=""
        else:
            account_name,seconds_account_name = account_t.fullname.split("-")

        t_detailInfo.account_name = account_name
        t_detailInfo.seconds_account_name = seconds_account_name

        t_detailInfo.save()



# 插入默认的用户：cc、mm
insert_default_user()
create_default_checkbook()
random_insert_details()
# 创建默认的记账本：CM家庭记账本