# -*- coding: UTF-8 -*-
from models.Models import UserInfo,AuthCode,UserCheckbookMap,CheckbookInfo
import base64
from utils import orm,db
import uuid
import datetime
import time
from utils import zaTools

def getCheckbookListByUser(user_name):
    """
    获得某个user名下的所有记账本
    :param user_name:
    :return:
    """
    checkbookList = []
    u = UserInfo.find_first("where name = ?", user_name);
    if not u:
        return checkbookList
    checkbookList = UserCheckbookMap.find_by("where user_id=%s  and permission>0",u.id)
    if not checkbookList:
        checkbookList=[]

    #3.转换格式
    restfulCHeckbook = []
    for ucm in checkbookList:
        dict_temp = {}
        dict_temp["checkbook_id"] = ucm.checkbook_id
        c = CheckbookInfo.find_first("where id=?",ucm.checkbook_id)
        dict_temp["name"] = c.name
        dict_temp["description"] = c.description
        dict_temp["is_local"] = c.islocal
        dict_temp["image_base64"] = c.coverImage
        ucMap = UserCheckbookMap.find_first("where user_id=? and checkbook_id=? and permission>0 ", u.id, c.id)
        dict_temp["permission"] = ucMap.permission
        #TODO 添加其他成员的名称
        dict_temp["other_member"] = []
        restfulCHeckbook.append(dict_temp)
    return restfulCHeckbook


def addCheckbook(user_name, checkbook_json):
    """新增一个记账本"""
    checkbook_id = checkbook_json.get("checkbook_id", zaTools.genID()),
    name = checkbook_json.get("name", ""),
    description = checkbook_json.get("description", ""),
    permission= checkbook_json.get("permission", 1),
    image_base64 =  checkbook_json.get("image_base64", ""),
    is_local = checkbook_json.get("is_local", 0),
    members = checkbook_json.get("other_member", [])

    u = UserInfo.find_first("where name = ?", user_name);
    if not u:
        return None

    #1. 创建checkbook对象，保存
    c = CheckbookInfo(id=checkbook_id, name=name, description=description, islocal=is_local, coverImage=image_base64)

    #2. 创建checkbook --user的映射，保存
    ucMap = UserCheckbookMap.find_first("where user_id=? and checkbook_id=? and permission>0 ",u.id,c.id)
    if not ucMap:
        ucMap = UserCheckbookMap(id=zaTools.genID(), user_id=u.id, checkbook_id=c.id, permission=permission, description="" )
    else:
        ucMap.permission=permission
        ucMap.description=""

    try:
        c.insert()
    except:
        c.update()
    try:
        ucMap.insert()
    except Exception as e:
        print(e)
        ucMap.update()
    return c.id


def deleteCheckbook(checkbook_id):
    """
    删除记账本
    :param checkbook_id:
    :return:
    """
    usm_list = UserCheckbookMap.find_by("where checkbook_id=? and  permission>0",checkbook_id)
    for usm in usm_list:
        usm.permission=0
        usm.update()
    return True



