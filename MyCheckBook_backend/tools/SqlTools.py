#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/29 14:39 
# @Author : wangchong 
# @Email: chongwangcc@gmail.com
# @File : SqlTools.py 
# @Software: PyCharm

import pandas as pd
import json
import copy
from datetime import datetime
from random import choice

from tools.Entity import *

g_sqlite3_path = "./data/sqlit3.db"
set_db_name(g_sqlite3_path)


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
            checkbook_list = []
            for checkbook in checkbooks:
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
                    if t_user.id == user_id:
                        t_check["my_permission"] = permission

                checkbook_list.append(t_check)
            return checkbook_list
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

    @classmethod
    def save_new_checkbook(cls, args, creator):
        """
        新建一个记账本
        :param args:
        :return:
        """
        checkbook = Checkbook()
        checkbook.checkbook_name = args["name"]
        checkbook.create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        checkbook.last_update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        checkbook.description = args["description"]
        checkbook.status = "正常"
        checkbook.partners = {}
        checkbook.partners["user_id-" + str(creator.id)] = "all"
        checkbook.partners = json.dumps(checkbook.partners)
        checkbook.creator = creator.id
        checkbook.save()
        return True


class DetailTools:
    """
    明细操作
    """

    @classmethod
    def create_detail(cls, detail_dict):
        """
        创建一条新的明细记录
        :param detail_dict:
        :return:
        """
        # TODO 0.检查参数格式是否正确

        # 1. 构造detail
        t_detail = DetailInfo()
        t_detail.date = detail_dict["date"]
        t_detail.month_str = t_detail.date[:7]
        t_detail.money = detail_dict["money"]
        t_detail.category = detail_dict["category"]
        t_detail.remark = detail_dict["remark"]
        t_detail.updater = UserTools.fetch_user_info(detail_dict["updater"]).id
        t_detail.checkbook = int(detail_dict["checkbook_id"])
        t_detail.type = detail_dict["type"]
        t_detail.isCash = detail_dict["isCash"]
        if "-" not in detail_dict["account_name"] :
            account_name = detail_dict["account_name"]
            seconds_account_name=""
        else:
            account_name,seconds_account_name = detail_dict["account_name"].split("-")
        t_detail.account_name = account_name
        t_detail.seconds_account_name = seconds_account_name
        t_detail.combine_details = json.dumps([])

        # 2.判断要不要创建关联的流入、流出项目
        t_detail_rel = None
        if t_detail.type == "支出" and t_detail.isCash == "现金":
            # 新建一笔关联的流出
            t_detail_rel = copy.deepcopy(t_detail)
            t_detail_rel.type = "流出"
            t_detail_rel = t_detail_rel.save()
            pass
        elif t_detail.type == "收入" and t_detail.isCash == "现金":
            # 新建一笔关联的流入
            t_detail_rel = copy.deepcopy(t_detail)
            t_detail_rel.type = "流出"
            t_detail_rel = t_detail_rel.save()
            pass

        # 设置 关联明细 的id
        t_detail = t_detail.save()
        if t_detail_rel is not None:
            t_detail.combine_details = json.dumps([t_detail_rel.id])
            t_detail_rel.combine_details = json.dumps([t_detail.id])
            t_detail_rel.save()
        # 2.保存
        t_detail = t_detail.save()
        return t_detail

    @classmethod
    def get_detail(cls, detail_id):
        """
        根据id获得明细 详情
        :param detail_id:
        :return:
        """
        detailinfo = DetailInfo.get(id=detail_id)
        t_detail = {}
        t_detail["detail_id"] = detailinfo.id
        t_detail["date"] = detailinfo.date
        t_detail["money"] = detailinfo.money
        t_detail["category"] = detailinfo.category
        t_detail["remark"] = detailinfo.remark
        t_detail["isCash"] = detailinfo.isCash
        t_detail["type"] = detailinfo.type
        t_detail["account_name"] = detailinfo.account_name
        t_detail["seconds_account_name"] = detailinfo.seconds_account_name
        t_detail["updater"] =detailinfo.updater.user_name
        t_detail["combine_details"] = detailinfo.combine_details
        t_detail["checkbook_name"] = Checkbook.get(id=detailinfo.checkbook).checkbook_name
        t_detail["checkbook_id"] =detailinfo.checkbook.id

        return t_detail

    @classmethod
    def delete_detail(cls, detail_id):
        """
        删除一条明细，会自动删除关联明细
        :param detail_id:
        :return:
        """
        # TODO 如果需要同步的化，要变成“标记删除”
        detail_info = DetailInfo.get(id=detail_id)
        try:
            related_id_list = json.loads(detail_info.combine_details)
            for m_id in related_id_list:
                try:
                    t_detail = DetailInfo.get(id=m_id)
                    t_detail.delete()
                except:
                    pass
        except:
            pass
        try:
            detail_info.delete()
        except:
            pass
        return True

    @classmethod
    def get_details_list(cls, checkbook_id, month_str, account_name=None, mtype=None, category=None):
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
                sql += " and " + " account_name == '" + str(account1) + "' "
            if account2 is not None:
                sql += " and " + " seconds_account_name == '" + str(account2) + "' "
        if mtype is not None:
            sql += " and " + " type == '" + str(mtype) + "' "
        if category is not None:
            sql += " and " + " category == '" + str(category) + "' "

        sql += " ORDER BY date DESC, id ASC "

        df = pd.read_sql_query(sql, conn)
        return df


if __name__ == "__main__":
    pass
    detias = get_Details(checkbook_id=1, month_str="2019-02")
    print(detias)



