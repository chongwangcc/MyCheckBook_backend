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
from tools.utils import *

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
    def fetch_all_checkbooks_full(cls, user_id):
        """
        获得所有记账本的详情
        :param user_id:
        :return:
        """
        checkbooks_json = CheckbookTools.fetch_all_checkbooks(user_id)
        checkbook_fulls_json = {}
        for checkbook in checkbooks_json:
            checkbook_id = checkbook["checkbook_id"]
            checkbook_fulls_json[checkbook_id] = CheckbookTools.get_checkbook_full(checkbook_id)
        return checkbook_fulls_json

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

    @classmethod
    def get_checkbook_account_list(cls, checkbook_id):
        account_list = []
        checkbook = Checkbook.get(id=checkbook_id)
        account_id_list = checkbook.account_id_list
        if account_id_list is not None and len(account_id_list) > 0:
            t_account_id_list = json.loads(account_id_list)
            for t_account_id in t_account_id_list:
                account_t = AccountInfo.get(id=t_account_id)
                account_list.append(account_t.fullname)
        return account_list


class DetailTools:
    """
    明细操作
    """

    @classmethod
    def create_detail(cls, detail_dict, is_edit=False):
        """
        创建一条新的明细记录
        :param detail_dict:
        :return:
        """
        # TODO 0.检查参数格式是否正确

        # 1. 构造detail
        t_detail = DetailInfo()
        if is_edit:
            t_detail.id = int(detail_dict["detail_id"])
            # TODO 性能问题，以后再改
            # 删除旧的明细表里相关联的记录
            old_details = DetailInfo.get(id=t_detail.id)
            if len(old_details.combine_details)>1:
                combine_detail_ids = json.loads(old_details.combine_details)
                for m_id in combine_detail_ids:
                    t_d = DetailInfo.get(id=m_id)
                    t_d.delete()
            old_details.delete()

        t_detail.date = detail_dict["date"]
        t_detail.month_str = t_detail.date[:7]
        t_detail.money = detail_dict["money"]
        t_detail.category = detail_dict["category"]
        t_detail.remark = detail_dict["remark"]
        t_detail.updater = UserTools.fetch_user_info(detail_dict["updater"]).id
        t_detail.checkbook = int(detail_dict["checkbook_id"])
        t_detail.type = detail_dict["type"]
        t_detail.isCash = detail_dict["isCash"]
        t_detail.updatetime = get_now_str()
        account_name, seconds_account_name = account_split(detail_dict["account_name"])
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
            account1, account2 = account_split(account_name)
            if account1 is not None and len(account1)>0:
                sql += " and " + " account_name == '" + str(account1) + "' "
            if account2 is not None and len(account1)>0:
                sql += " and " + " seconds_account_name == '" + str(account2) + "' "
        if mtype is not None:
            sql += " and " + " type == '" + str(mtype) + "' "
        if category is not None:
            sql += " and " + " category == '" + str(category) + "' "
        sql += " ORDER BY date DESC, id ASC "
        df = pd.read_sql_query(sql, conn)
        return df


class AssetsTools:

    @classmethod
    def get_tmm(cls):
        result = {}
        t_sum = {}
        t_sum["总资产"] = {
            "sum": 50980,
            "data": [
                {"name": "流动资产",
                 "sum": 300,
                 "data": [
                     {"银行卡": 100},
                     {"货币基金": 200},
                     {"手头现金": 300},
                 ]},
                {
                    "name": "固定资产",
                    "sum": 400,
                    "data": [
                        {"定期存款": 400},
                        {"外债资产": 500}
                    ]},
                {
                    "name": "投资资产",
                    "sum": 500,
                    "data": [
                        {"股票资产": 400},
                        {"定投资产": 6000}
                    ]
                }
            ],
        }
        t_sum["总负债"] = {
            "sum": 5090,
            "data": [
                {
                    "name": "流动负债",
                    "sum": 300,
                    "data": [
                        {"信用卡": 100},
                        {"欠朋友": 200},
                    ]
                },
                {
                    "name": "长期负债",
                    "sum": 400,
                    "data": [
                        {"信用卡": 400},
                    ]
                },
                {
                    "name": "投资负债",
                    "sum": 500,
                    "data": [
                        {"股票杠杆": 400},
                    ]
                }
            ],
        }
        result["sum"] = {
            "合并账户": t_sum,
            "花销账户": t_sum,
            "投资账户": t_sum,
            "储蓄账户": t_sum,
        }
        t_appendix = {}
        t_appendix["银行卡"] = [
            {"name": "建行银行卡（CC）", "money": 1234, "account": "花销账户-Doodads账户"},
            {"name": "建行银行卡（MM）", "money": 1234, "account": "花销账户-Doodads账户"},
        ]
        t_appendix["货币基金"] = [
            {"name": "支付宝-余额宝", "money": 1234, "account": "花销账户-Doodads账户"},
            {"name": "理财通-余额+", "money": 1234, "account": "花销账户-Doodads账户"},
        ]
        t_appendix["信用卡"] = [
            {"name": "支付宝-花呗", "money": 1234, "account": "花销账户-Doodads账户"},
            {"name": "信用卡-建行（CC）", "money": 1234, "account": "花销账户-Doodads账户"},
        ]
        result["appendix"] = t_appendix
        return result
        pass

    @classmethod
    def get_assets_full(cls, checkbook_id, month_str, action="ALL"):
        """
        获得assets 全部内容
        :param checkbook_id:
        :param month_str:
        :param action:
        :return:
        """
        result = {}
        t_appendix = AppendixTools.get_appendix_name_list(checkbook_id, month_str)
        if action == "appendix" or action == "ALL":
            result["appendix"]= t_appendix
        if action == "SUM" or action == "ALL":
            sum_entity = AssetsSumUtils(CheckbookTools.get_checkbook_account_list(checkbook_id))
            for name, appendix in t_appendix.items():
                t_row = appendix["rows"]
                t_columns = appendix["columns"]
                t_content = appendix["content"]
                t_df = pd.DataFrame(t_content)
                #  遍历df, 计算各类汇总
                for index, row in t_df.iterrows():
                    if name in ["信用卡负债"]:
                        sum_entity.add(row["当月应还（元）"],
                                       row["当月应还（元）"],
                                       name,
                                       row["所属账户"],
                                       "流动负债")
                        sum_entity.add(row["总欠款（元）"]-row["当月应还（元）"],
                                       row["总欠款（元）"] - row["当月应还（元）"],
                                       name,
                                       row["所属账户"],
                                       "长期负债")
                    else:
                        sum_entity.add(row["原价"],
                                       row["现价"],
                                       name,
                                       row["所属账户"],
                                       row["流动性"])
            result["sum"] = sum_entity.get_final_result()
        if action == "empty":
            result["empty"] = AppendixTools.get_empty_appendix(checkbook_id)



        return result


class AppendixTools:

    @classmethod
    def get_appendix_df(cls, checkbook_id, month_str, appendix_name):
        """
        获得一个附表记录的数据，转换为dataframe。
        数据库中应该是唯一的一条记录
        :param checkbook_id:
        :param month_str:
        :param appendix_name:
        :return:
        """
        old_append_info = AppendixInfo.get(checkbook=checkbook_id,
                                           month_str=month_str,
                                           appendix_name=appendix_name)
        rows = json.loads(old_append_info.row_json)
        columns = json.loads(old_append_info.columns_json)
        content = json.loads(old_append_info.content_json)
        df = pd.DataFrame(content)

        return df, rows, columns

    @classmethod
    def get_appendix_name_list(cls, checkbook_id, month_str):
        """
        获得某月的附表所有名称
        :param checkbook_id:
        :param month_str:
        :return:
        """
        old_append_infos = AppendixInfo.gets(checkbook=checkbook_id,
                                           month_str=month_str)
        result = {}
        for info in old_append_infos:
            rows = json.loads(info.row_json)
            columns = json.loads(info.columns_json)
            content = json.loads(info.content_json)
            result[info.appendix_name] = {
                "rows": rows,
                "columns": columns,
                "content": content
            }
        return result

    @classmethod
    def get_empty_appendix(cls, checkbook_id):
        """
        制作财报时使用，获得一张空内容的附表记录，去掉金额的。
        :param checkbook_id:
        :param month_str:
        :return:
        """
        #  获得最近的附录
        month_str = AppendixInfo.get_lastest_month()
        if month_str is None:
            return None
        old_append_infos = AppendixInfo.gets(checkbook=checkbook_id,
                                           month_str=month_str)
        # 将其中的金额 变成0
        result = {}
        money_names = ["原价", "现价", "总欠款（元）", "当月应还（元）"]
        for info in old_append_infos:
            rows = json.loads(info.row_json)
            columns = json.loads(info.columns_json)
            content = json.loads(info.content_json)
            for m in money_names:
                if m not in columns:
                    continue
                c = content.setdefault(m, {})
                new_c = {}
                for key, value in c.items():
                    new_c[key] = 0
                content[m] = new_c

            result[info.appendix_name] = {
                "rows": rows,
                "columns": columns,
                "content": content
            }
        return result

    @classmethod
    def save_appendix(cls, checkbook_id, month_str, appendix_name, df, name="名称"):
        """
        保存一个附表
        :param checkbook_id:
        :param month_str:
        :param appendix_name:
        :param df:
        :return:
        """
        columns = list(df.columns)
        name_rows = []
        if len(df) > 0:
            name_rows = list(df[name])
        content = df.to_dict(orient="dict")

        # 1.判断有没有旧的值
        append_info = AppendixInfo()
        old_append_info = AppendixInfo.get(checkbook=checkbook_id,
                                           month_str=month_str,
                                           appendix_name=appendix_name)
        # 之前有值得话，覆盖之前的值
        if old_append_info is not None:
            append_info.id = old_append_info.id


        append_info.checkbook = checkbook_id
        append_info.month_str = month_str
        append_info.appendix_name = appendix_name
        append_info.row_json = json.dumps(name_rows)
        append_info.columns_json = json.dumps(columns)
        append_info.content_json = json.dumps(content)
        append_info.update_time_str = get_now_str()
        append_info.save()
        return True

    @classmethod
    def delete_appendix(cls, checkbook_id, month_str):
        """
        删除相关附表
        :param checkbook_id:
        :param month_str:
        :return:
        """
        AppendixInfo.delete_all(checkbook_id, month_str)






if __name__ == "__main__":
    # ree = CheckbookTools.get_checkbook_account_list(1)
    # print(ree)
    # pass
    # detias = get_Details(checkbook_id=1, month_str="2019-02")
    # print(detias)
    # result = AppendixTools.get_appendix_name_list(1, "2019-03")
    # print(result)
    print(AppendixTools.get_empty_appendix(1))





