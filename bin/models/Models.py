# -*- coding: UTF-8 -*-

from utils.orm import Model,StringField,IntegerField,FloatField,TextField


class UserInfo(Model):
    """
    用户信息表
    """
    __table__ = "UserInfo"
    id = StringField(primary_key=True)
    name = StringField()
    password = StringField()
    description = StringField()
    pass


class CheckbookInfo(Model):
    """
    记账本信息
    """
    __table__ = "CheckbookInfo"
    id = StringField(primary_key=True)
    name = StringField()
    description = StringField()
    islocal = IntegerField()
    coverImage = TextField()
    pass


class AccountInfo(Model):
    """
    账户信息
    """
    __table__ = "AccountInfo"
    account_id = StringField(primary_key=True)
    account_name = StringField()
    parent_id = StringField()
    level = IntegerField()
    assets_nums = FloatField()
    liabilities_nums = FloatField()
    pass


class DetailsInfo(Model):
    """
    记账明细信息
    """
    __table__ = "CheckDetails"
    id = StringField(primary_key=True)
    checkbook_id = StringField()
    account_id = StringField()
    last_update_user_id = StringField()
    date_str = StringField()
    year = StringField()
    month = StringField()
    day = StringField()
    money = IntegerField()
    description = StringField()
    balanceType = StringField()
    Category = StringField()
    isCreditcard = StringField()
    updateTime = IntegerField()
    createTime = IntegerField()
    pass


class AuthCode(Model):
    """
    授权码类
    """
    __table__ = "AuthCode"
    auth_code=StringField(primary_key=True)
    user_id = StringField()
    endDate = IntegerField()
    permission = IntegerField()


class CheckbookAccountMap(Model):
    """
    记账本与账户映射关系类
    """
    __table__ = "CheckbookAccountMap"
    id=StringField(primary_key=True)
    checkbook_id=StringField()
    user_id = StringField()


class Invitation(Model):
    """
    邀请码关系类
    """
    __table__ = "Invitation"
    invitation_code=StringField(primary_key=True)
    checkbook_id = StringField()
    permission = IntegerField()
    total_member_nums = IntegerField()
    used_member_nums = IntegerField()


class UserCheckbookMap(Model):
    """
    邀请码关系类
    """
    __table__ = "UserCheckbookMap"
    id = StringField(primary_key=True)
    user_id=StringField()
    checkbook_id = StringField()
    permission = IntegerField()
    description = StringField()