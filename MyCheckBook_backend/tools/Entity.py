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

class User_Info(Model, UserMixin):
    """
    用户信息表
    """
    user_name = CharField(128)
    password = CharField(128)
    active = IntegerField()
    auth_token_file = CharField(256)
    calender_server = CharField(128)
    calender_name = CharField(128)
    email = CharField(128)

    def get_id(self):
        return self.user_name

    def get_by_id(self, user_name):
        try:
            userinfo = User_Info.get(user_name=user_name)
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
    def is_user_exist():
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
                return True
        except:
            lock.release()
            pass
        return False


if __name__ == "__main__":

    g_sqlite3_path = "./data/sqlit3.db"
    set_db_name(g_sqlite3_path)
    userinfo = User_Info()
    userinfo.user_name="cc"
    userinfo.password="123456"
    userinfo.active=1
    userinfo.auth_token_file = r".\data\.credentials\cc_calendar.json"
    userinfo.calender_server = "google"
    userinfo.calender_name = "时间日志"
    userinfo.save()

    userinfo = User_Info()
    userinfo.user_name="mm"
    userinfo.password="123456"
    userinfo.active=1
    userinfo.auth_token_file = r".\data\.credentials\mm_calendar.json"
    userinfo.calender_server = "google"
    userinfo.calender_name = "时间日志"
    userinfo.save()


    # userinfo = User_Info.get(user_name="cc")
    # userinfo.delete()
    # userinfo = User_Info.get(user_name="mm")
    # userinfo.delete()
    # print(userinfo)

    userinfo = User_Info.get(user_name="cc")
    print(userinfo.to_dict())
    print(userinfo)

