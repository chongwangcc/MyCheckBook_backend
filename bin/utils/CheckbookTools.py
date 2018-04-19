# -*- coding: UTF-8 -*-
from models.Models import UserInfo,UserCheckbookMap,CheckbookInfo,Invitation

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
        c = CheckbookInfo.find_first("where id=?", ucm.checkbook_id)
        dict_temp= convertCheckbookFromMysqlToRestful(u,c)
        restfulCHeckbook.append(dict_temp)
    return restfulCHeckbook


def addCheckbook(user_name, checkbook_json):
    """新增一个记账本"""
    checkbook_id = checkbook_json.get("checkbook_id", zaTools.genID())
    name = checkbook_json.get("name", "")
    description = checkbook_json.get("description", "")
    permission= checkbook_json.get("permission", 1)
    image_base64 =  checkbook_json.get("image_base64", "")
    is_local = checkbook_json.get("is_local", 0)
    members = checkbook_json.get("other_member", [])

    u = UserInfo.find_first("where name = ?", user_name)
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


def getCheckbookByID(user_name,checkbook_id):
    """
    通过id获得checkbook结构
    :param user_name:
    :param checkbook_id:
    :return:
    """
    checkbook=None
    #1. 检查user有没有此项id的操作权限
    u = UserInfo.find_first("where name = ?", user_name);
    if not u:
        return checkbook
    ucMap = UserCheckbookMap.find_first("where user_id=? and checkbook_id=? and permission>0 ", u.id, checkbook_id)
    if not ucMap:
        return checkbook
    checkbook = CheckbookInfo.find_first("where id=?", checkbook_id)
    resutlf =convertCheckbookFromMysqlToRestful(u,checkbook)
    return resutlf


def convertCheckbookFromMysqlToRestful(user_info,checkbook_mysql):
    """
    转化数据格式
    :param user_info:
    :param checkbook_mysql:
    :return:
    """
    dict_temp = {}
    dict_temp["checkbook_id"] = checkbook_mysql.id
    dict_temp["name"] = checkbook_mysql.name
    dict_temp["description"] = checkbook_mysql.description
    dict_temp["is_local"] = checkbook_mysql.islocal
    dict_temp["image_base64"] = checkbook_mysql.coverImage
    ucMap = UserCheckbookMap.find_first("where user_id=? and checkbook_id=? and permission>0 ", user_info.id, checkbook_mysql.id)
    dict_temp["permission"] = ucMap.permission
    # TODO 添加其他成员的名称
    dict_temp["other_member"] = []
    return dict_temp


def makeupInvitation(user_name,auth_code,checkbook_id,nums,permission):
    """
    生成邀请码
    :return:
    """
    #1.检查是否有创建的权限
    invitation=None
    u = UserInfo.find_first("where name = ?", user_name);
    if not u:
        return invitation
    ucMap = UserCheckbookMap.find_first("where user_id=? and checkbook_id=? and permission>0 ", u.id, checkbook_id)
    if not ucMap:
        return invitation
    #2.生成Invitation 保存
    inv = Invitation(invitation_code=zaTools.genID(),checkbook_id=checkbook_id,permission=permission,total_member_nums=nums,used_member_nums=0)
    inv.insert()
    return inv.invitation_code


def joinCheckbooks(user_name,invitation):
    """
    使用邀请码加入一个checkbook中
    :param invitation:
    :param user_name:
    :return:
    """
    checkbook=None
    u = UserInfo.find_first("where name = ?", user_name);
    if not u:
        return checkbook
    invi = Invitation.find_first("where invitation_code=?",invitation)
    if not invi:
        return checkbook
    invi.used_member_nums=invi.used_member_nums+1
    if invi.used_member_nums>invi.total_member_nums:
        return checkbook

    ucMap = UserCheckbookMap.find_first("where user_id=? and checkbook_id=? and permission>0 ", u.id, invi.checkbook_id)
    if not ucMap:
        ucMap = UserCheckbookMap(id=zaTools.genID(), user_id=u.id, checkbook_id=invi.checkbook_id, permission=invi.permission,
                                 description="")
    try:
        ucMap.insert()
    except Exception as e:
        print(e)
        ucMap.update()
    try:
        invi.insert()
    except Exception as e:
        print(e)
        invi.update()
    return getCheckbookByID(user_name,invi.checkbook_id)

