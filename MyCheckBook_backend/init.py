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
import pandas as pd

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


def intert_category_info():
    """
    插入几个类别描述
    :return:
    """
    mtypes= {
        "收入":["工资", "利息","证券投资","家里给","奖金", "兼职所得"],
        "支出":["零食", "餐饮","住房","通讯","社交","运动"],
        "流入":["购物返现"],
        "流出":["还信用卡"]
    }
    if CategoryInfo.is_empty():
        pass
        for key,value in mtypes.items():
            for v in value:
                c =  CategoryInfo()
                c.type = key
                c.name = v
                c.belong_checkbook=1
                c.save()


def insert_appendix_info():
    """
    插入一些附表的值
    :return:
    """
    checkbook_id = 1
    month_str = "2019-03"

    # 1.银行卡
    # 名称，金额，开户人，备注
    data = {
        "名称": ["建设银行（0781）",
               "交通银行（9889）",
               "农业银行（5378）",
               "工商银行（8915）",
               "民生银行（3988）",
               "招商银行（8115）",
               "交通银行（6436）",
               "建设银行（4704）"],
        "原价": [1.71, 216.98, 0, 0, 1197.85, 0, 0.96, 82.04],
        "现价": [1.71, 216.98, 0, 0, 1197.85, 0, 0.96, 82.04],
        "所属账户": ["投资账户-现金储备",
                 "花销账户-生活费",
                 "花销账户-生活费",
                 "花销账户-生活费",
                 "花销账户-生活费",
                 "花销账户-生活费",
                 "花销账户-生活费",
                 "花销账户-生活费"
                 ],
        "流动性": ["流动资产", "流动资产", "流动资产", "流动资产", "流动资产", "流动资产", "流动资产", "流动资产"],
        "开户人": ["王翀", "王翀", "王翀", "王翀", "张文慧", "张文慧", "张文慧", "张文慧"],
        "备注": ["", "", "", "","", "", "", ""]
    }
    df_card = pd.DataFrame(data)
    print(df_card)
    AppendixTools.save_appendix(1, "2019-03", "银行卡", df_card)

    # 2.货币基金
    # 名称，金额，开户人，备注
    data = {
        "名称": ["支付宝-余额宝",
               "支付宝-招商招利宝A",
               "支付宝-余利宝",
               "支付宝-天弘弘运货币B",
               "支付宝-富国钱包",
               "支付宝-余额",
               "微信-余额+(CC)",
               "微信-余额+(MM)",
               "微信-零钱(MM)",
               "微信-零钱理财",
               "招行-招招盈"],
        "原价": [317.64, 13804.48, 18016.28, 16811.03, 219.12, 0, 32112.74, 74736.14, 0, 1424.7, 24118.47],
        "现价": [317.64, 13804.48, 18016.28, 16811.03, 219.12, 0, 32112.74, 74736.14, 0, 1424.7, 24118.47],
        "所属账户": ["花销账户-生活费",
                 "花销账户-住房基金",
                 "花销账户-生活费",
                 "花销账户-风险备付金",
                 "花销账户-doodads",
                 "花销账户-生活费",
                 "储蓄账户-现金储备",
                 "投资账户-现金储备",
                 "花销账户-生活费",
                 "花销账户-生活费",
                 "花销账户-教育基金"],
        "流动性": ["流动资产", "流动资产", "流动资产", "流动资产","流动资产", "流动资产", "流动资产", "流动资产","流动资产", "流动资产", "流动资产"],
        "开户人": ["王翀", "王翀", "王翀", "王翀","王翀","王翀","王翀", "张文慧","张文慧","张文慧","张文慧"],
        "备注": ["", "", "", "","", "", "", "","", "", ""]
    }
    for key,value in data.items():
        print(key+"  "+str(len(value)))
    df_card = pd.DataFrame(data)
    print(df_card)
    AppendixTools.save_appendix(1, "2019-03", "货币基金", df_card)

    # 3.外债资产
    # 债务人名称，金额，归还日期，备注
    data = {
        "名称": ["DMCC",
               "东方园林",
               "王书明"],
        "原价": [10000, 19700, 20000],
        "现价": [10000, 19700, 20000],
        "所属账户": ["储蓄账户",
                 "储蓄账户",
                 "储蓄账户"
                 ],
        "流动性": ["固定资产", "固定资产", "固定资产"],
        "归还日期": ["2019.7.1", "", "2029.2.1"],
        "备注": ["2个月押金", "年终奖欠款（税前为23103）", ""]
    }
    df_card = pd.DataFrame(data)
    print(df_card)
    AppendixTools.save_appendix(1, "2019-03", "外债资产", df_card)

    # 4.押金资产
    # 名称，金额，归还日期，备注
    data = {
        "名称": ["租房押金",
               "国家图书馆",
               "首都图书馆",
               "地铁卡",
               "水桶押金"],
        "原价": [5200, 100, 100, 40, 50],
        "现价": [5200, 100, 100, 40, 50],
        "所属账户": ["储蓄账户",
                 "储蓄账户",
                 "储蓄账户",
                 "储蓄账户",
                 "储蓄账户",
                 ],
        "流动性": ["固定资产", "固定资产", "固定资产",  "固定资产", "固定资产"],
        "归还日期": ["2019.7.1", "", "","","2029.2.1"],
        "备注": ["", "","","", "桶装水"]
    }
    df_card = pd.DataFrame(data)
    print(df_card)
    AppendixTools.save_appendix(1, "2019-03", "押金资产", df_card)

    # 5. 投资资产
    # 名称，本金，市值，可用资金，备注
    data = {
        "名称": ["股票（中信证券）",
               "股票（信达证券）",
               "基金（创业板指数定投-张文慧）",
               ],
        "原价": [10000, 32000, 77500],
        "现价": [9120, 20438, 77551.51],
        "可用资金": [2519.08, 4975.53, 0],
        "所属账户": ["投资账户-股票账户",
                 "投资账户-股票账户",
                 "投资账户-股票账户",
                 ],
        "流动性": ["投资资产", "投资资产", "投资资产"],
        "备注": ["", "", ""]
    }
    df_card = pd.DataFrame(data)
    print(df_card)
    AppendixTools.save_appendix(1, "2019-03", "投资资产", df_card)

    # 6. 信用卡负债
    # 名称，总欠款，当月应还，开户人，备注
    data = {
        "名称": ["建行信用卡（9231）",
               "中行信用卡（1261）",
               "蚂蚁花呗",
               "广发信用卡（0568）",
               "微信微粒贷（CC）",
               "微信微粒贷(MM)",
               "支付宝-花呗备付金",
               ],
        "总欠款（元）": [168.02, 25.77, 6927.6, 474, 0, 66000, 0],
        "当月应还（元）": [168.02, 25.77, 4154.46, 470, 0, 66000, 0],
        "开户人": ["王翀", "王翀", "王翀", "张文慧", "王翀", "张文慧", "王翀"],
        "所属账户": ["花销账户-生活费",
                 "花销账户-生活费",
                 "花销账户-生活费",
                 "花销账户-生活费",
                 "投资账户-股票账户",
                 "投资账户-股票账户",
                 "投资账户-股票账户",
                 ],
        "流动性": ["负债", "负债", "负债 ", "负债 ", "投资负债", "投资负债","投资负债"],
        "备注": ["", "", "","", "", "",""]
    }
    for key,value in data.items():
        print(key+"  "+str(len(value)))
    df_card = pd.DataFrame(data)
    print(df_card)
    AppendixTools.save_appendix(1, "2019-03", "信用卡负债", df_card)
    # 7. 手头现金
    # 名称金额
    data = {
        "名称": ["mm钱包",
               "CC钱包",
               "家中备用现金",
               ],
        "原价": [1400, 130, 10000],
        "现价": [1400, 130, 10000],
        "所属账户": ["花销账户-生活费",
                 "花销账户-生活费",
                 "花销账户-生活费",
                 ],
        "流动性": ["流动资产", "流动资产", "流动资产"],
        "备注": ["", "", ""]
    }
    df_card = pd.DataFrame(data)
    print(df_card)
    AppendixTools.save_appendix(1, "2019-03", "手头现金", df_card)

    # 8. 定期资产
    # 名称，金额，到期日，开户人，备注
    data = {
        "名称": ["建行存单"],
        "原价": [10000],
        "现价": [10000],
        "到期日": ["2019.7.10"],
        "开户人": ["王翀"],
        "所属账户": ["花销账户-风险备付金"],
        "流动性": ["流动资产"],
        "备注": [""]
    }
    df_card = pd.DataFrame(data)
    print(df_card)
    AppendixTools.save_appendix(1, "2019-03", "定期资产", df_card)

    # 9. 预付款资产
    # 名称，金额，收货日期，供应商名称，备注
    data = {
        "名称": [],
        "原价": [],
        "现价": [],
        "收获日期": [],
        "供应商名称": [],
        "所属账户": [],
        "流动性": [],
        "备注": []
    }
    df_card = pd.DataFrame(data)
    print(df_card)
    AppendixTools.save_appendix(1, "2019-03", "预付款资产", df_card)


def insert_report_info():
    checkbook_id = 1
    period = ["2019.03.01-2019.03.31","2019.02.01-2019.02.31","2019.04.01-2019.04.30"]

    for p in period:
        info = ReportInfo()
        info.report_name = "2019-03-家庭月报"
        info.mtype = "月报"
        info.period = p
        info.checkbook=1
        info.owner = "CC&&MM"
        info.career = "程序员&&创业者"
        info.auditor = "CC"
        info.suggestion = "Doodads欠款太多，要节制。投资账户钱一直在趴着，多利用下"
        info.create_date = "2019-03-01"
        info.report_file_path = ""
        info.save()

# 插入默认的用户：cc、mm
# insert_default_user()
# create_default_checkbook()
# random_insert_details()
# intert_category_info()
insert_report_info()
# 创建默认的记账本：CM家庭记账本