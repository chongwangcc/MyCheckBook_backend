#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/30 10:18 
# @Author : wangchong 
# @Email: chongwangcc@gmail.com
# @File : Entity.py 
# @Software: PyCharm
from nanorm import *
from flask_login import UserMixin, AnonymousUserMixin


# 内存中的 实体结果 ---------------------


# SQLite 数据库中 实体结构定义---------------------------

class UserInfo(Model, UserMixin):
    """
    用户信息表
    """
    user_name = CharField(128)
    password = CharField(128)
    active = IntegerField()
    email = CharField(128)

    def get_id(self):
        return self.user_name

    def get_by_id(self, user_name):
        try:
            userinfo = UserInfo.get(user_name=user_name)
            return userinfo
        except:
            pass
        return None

    def __str__(self):
        return str(self.to_dict())

    def to_dict(self):
        dict_my = {}
        for key, value in zip(self.field_names,self.field_values):
            dict_my[key.replace("`", "")] = value.replace("'", "")
        return dict_my

    @staticmethod
    def is_empty():
        """
        判断user_info表是否为空
        :return:
        """
        try:
            sql = "select * from %s limit 1" \
                  % (__class__.__name__.lower())
            cu = get_cursor()
            execute_sql(cu, sql)
            rows = cu.fetchall()
            if len(rows) >= 1 :
                return False
        except:
            lock.release()
            pass
        return True


class Checkbook(Model):
    """
    一个记账本记录
    """
    checkbook_name = CharField(128)  # 记账本描述
    create_time = CharField(20)  # 创建时间
    last_update_time = CharField(20)  # 最后更新时间
    description = CharField(128)  # 记账本描述
    partners = CharField(128)  # 参与者，共同编辑者
    status = CharField(128)  # 状态：正常、封账、禁用
    creator = ForeignKey(UserInfo)  # 创建者
    account_id_list = CharField()  # 所有账户的id

    def __str__(self):
        return str(self.to_dict())

    def to_dict(self):
        dict_my = {}
        for key, value in zip(self.field_names,self.field_values):
            dict_my[key.replace("`", "")] = value.replace("'", "")
        return dict_my

    @staticmethod
    def is_empty():
        """
        判断user_info表是否为空
        :return:
        """
        try:
            sql = "select * from %s limit 1" \
                  % (__class__.__name__.lower())
            cu = get_cursor()
            execute_sql(cu, sql)
            rows = cu.fetchall()
            if len(rows) >= 1 :
                return False
        except:
            lock.release()
            pass
        return True


class CategoryInfo(Model):
    """
    描述分类的类别
    """
    type = CharField(8) # 类别：收入、支出、流入、流出
    name = CharField()
    belong_checkbook = ForeignKey(Checkbook)
    image_base64 = CharField() # 图片logo的base64编码

    def __str__(self):
        return str(self.to_dict())

    def to_dict(self):
        dict_my = {}
        for key, value in zip(self.field_names,self.field_values):
            dict_my[key.replace("`", "")] = value.replace("'", "")
        return dict_my

    @staticmethod
    def is_empty():
        """
        判断user_info表是否为空
        :return:
        """
        try:
            sql = "select * from %s limit 1" \
                  % (__class__.__name__.lower())
            cu = get_cursor()
            execute_sql(cu, sql)
            rows = cu.fetchall()
            if len(rows) >= 1 :
                return False
        except:
            lock.release()
            pass
        return True


class AccountInfo(Model):
    """
    账户信息
    """
    name = CharField()
    fullname = CharField()
    parent_acccount = IntegerField()
    children_account = CharField()
    supportType = CharField()
    isGenRport=BooleanField()
    description = CharField()
    belong_checkbook = ForeignKey(Checkbook)

    def __str__(self):
        return str(self.to_dict())

    def to_dict(self):
        dict_my = {}
        for key, value in zip(self.field_names,self.field_values):
            dict_my[key.replace("`", "")] = value.replace("'", "")
        return dict_my

    @staticmethod
    def is_empty():
        """
        判断user_info表是否为空
        :return:
        """
        try:
            sql = "select * from %s limit 1" \
                  % (__class__.__name__.lower())
            cu = get_cursor()
            execute_sql(cu, sql)
            rows = cu.fetchall()
            if len(rows) >= 1 :
                return False
        except:
            lock.release()
            pass
        return True


class DetailInfo(Model):
    """
    一条明细记录
    """
    date = CharField(128)  # 日期
    money = FloatField()  # 金额
    category = CharField(16)  # 类别
    month_str = CharField(7)
    remark = CharField(128)  # 备注
    isCash = CharField(16)  # 是否是现金
    type = CharField(16)  # 支出/收入/流入/流出
    checkbook = ForeignKey(Checkbook)  # 归属记账本
    account_name = CharField(128)  # 账户名
    seconds_account_name = CharField(128)  # 二级账户名
    updater = ForeignKey(UserInfo)  # 创建者
    updatetime = CharField(20)  # 更新时间
    combine_details = CharField()  # 组合的记账本明细
    activity_names = CharField()  # 活动名称

    def __str__(self):
        return str(self.to_dict())

    def to_dict(self):
        dict_my = {}
        for key, value in zip(self.field_names,self.field_values):
            dict_my[key.replace("`", "")] = value.replace("'", "")
        return dict_my

    @staticmethod
    def get_table_name():
        return __class__.__name__.lower()

    @staticmethod
    def is_empty():
        """
        判断user_info表是否为空
        :return:
        """
        try:
            sql = "select * from %s limit 1" \
                  % (__class__.__name__.lower())
            cu = get_cursor()
            execute_sql(cu, sql)
            rows = cu.fetchall()
            if len(rows) >= 1 :
                return False
        except:
            lock.release()
            pass
        return True


class AppendixInfo(Model):
    """
    附表信息类
    """
    checkbook = ForeignKey(Checkbook)  # 归属记账本
    month_str = CharField(7)
    appendix_name = CharField()
    row_json = CharField()
    columns_json = CharField()
    content_json = CharField()
    update_time_str = CharField()

    def __str__(self):
        return str(self.to_dict())

    def to_dict(self):
        dict_my = {}
        for key, value in zip(self.field_names,self.field_values):
            dict_my[key.replace("`", "")] = value.replace("'", "")
        return dict_my

    @staticmethod
    def get_table_name():
        return __class__.__name__.lower()

    @classmethod
    def get_lastest_month(cls):
        """
        最近的month_str
        :param self:
        :return:
        """
        try:
            sql = "select month_str from " + cls.get_table_name() + "  order by month_str DESC limit 1"
            cu = get_cursor()
            execute_sql(cu, sql)
            rows = cu.fetchall()
            return rows[0][0]
        except:
            lock.release()
        return None

    @classmethod
    def delete_all(cls, checkbook_id, month_str):
        try:
            sql = "delete from " + cls.get_table_name() \
                  + " where checkbook_id="+checkbook_id \
                  + " and month_str='"+ month_str + "'"
            cu = get_cursor()
            execute_sql(cu, sql)
            return True
        except:
            lock.release()
        return False

    @staticmethod
    def is_empty():
        """
        判断user_info表是否为空
        :return:
        """
        try:
            sql = "select * from %s limit 1" \
                  % (__class__.__name__.lower())
            cu = get_cursor()
            execute_sql(cu, sql)
            rows = cu.fetchall()
            if len(rows) >= 1 :
                return False
        except:
            lock.release()
            pass
        return True


class ReportInfo(Model):
    """
    财报的相关字段
    """
    checkbook = ForeignKey(Checkbook)  # 归属记账本
    mtype = CharField(16)
    period = CharField(32)
    owner = CharField(32)
    career = CharField(32)
    auditor = CharField(32)
    suggestion = CharField()
    create_date = CharField()
    report_file_path = CharField()

    def __str__(self):
        return str(self.to_dict())

    def to_dict(self):
        dict_my = {}
        for key, value in zip(self.field_names,self.field_values):
            dict_my[key.replace("`", "")] = value.replace("'", "")
        return dict_my

    @staticmethod
    def get_table_name():
        return __class__.__name__.lower()


    @staticmethod
    def is_empty():
        """
        判断user_info表是否为空
        :return:
        """
        try:
            sql = "select * from %s limit 1" \
                  % (__class__.__name__.lower())
            cu = get_cursor()
            execute_sql(cu, sql)
            rows = cu.fetchall()
            if len(rows) >= 1 :
                return False
        except:
            lock.release()
            pass
        return True






