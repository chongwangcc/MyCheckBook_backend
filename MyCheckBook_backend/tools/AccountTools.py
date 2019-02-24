# -*- coding: UTF-8 -*-
from models.Models import CheckbookAccountMap,AccountInfo

from tools import zaTools


def getAccountList(checkbook_id):
    """
    获得某个记账本下的所有账户
    :param checkbook_id:
    :return:
    """
    account_list=[]
    caMap = CheckbookAccountMap.find_by("where checkbook_id = ?",checkbook_id)
    for ca in caMap:
        account_id = ca.account_id
        aInfo = getAccountInfo(account_id)
        aInfo = convertAccountFromMysqlToRestful(aInfo)
        account_list.append(aInfo)

    return account_list

def getAccountInfo(account_id):
    """
    获得account的mysql结构
    :param account_id:
    :return:
    """
    aInfo = AccountInfo.find_first("where account_id =?",account_id)
    return aInfo

def deleteAccountInfo(account_id):
    """
    删除accountInfo
    :param account_id:
    :return:
    """
    caMap = CheckbookAccountMap.find_by("where account_id = ?", account_id)
    for ca in caMap:
        ca.delete()
    account_list = AccountInfo.find_by("where account_id = ?", account_id)
    for acount in account_list:
        acount.delete()
    return True


def addAccountInfo(checkbook_id,account_json):
    """
    添加account信息
    :param checkbook_id:
    :param account_json:
    :return:
    """
    account_id = account_json.get("account_id", zaTools.genID())
    account_name = account_json.get("account_name", "")
    parent_id = account_json.get("parent_id", "")
    assets_nums = account_json.get("assets_nums", 1)
    liabilities_nums = account_json.get("liabilities_nums", "")
    image_base64 = account_json.get("image_base64", 0)

    caMap = CheckbookAccountMap.find_by("where account_id = ?", account_id)
    if not caMap:
        caMap=CheckbookAccountMap(id=zaTools.genID(),checkbook_id=checkbook_id,account_id=account_id)
    account = AccountInfo(account_id=account_id,account_name=account_name,parent_id=parent_id,assets_nums=assets_nums,liabilities_nums=liabilities_nums)
    try:
        account.insert()
    except Exception as e:
        print(e)
        account.update()
    try:
        caMap.insert()
    except Exception as e:
        print(e)
        caMap.update()
    return account


def convertAccountFromMysqlToRestful(account_mysql):
    """
    转换account类型
    :param account_mysql:
    :return:
    """
    dict_temp={}
    dict_temp["account_id"]=account_mysql.account_id
    dict_temp["account_name"] = account_mysql.account_name
    dict_temp["parent_id"] = account_mysql.parent_id
    dict_temp["assets_nums"] = account_mysql.assets_nums
    dict_temp["liabilities_nums"] = account_mysql.liabilities_nums
    return dict_temp