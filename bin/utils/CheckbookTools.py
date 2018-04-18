# -*- coding: UTF-8 -*-
from models.Models import UserInfo,AuthCode,UserCheckbookMap
from utils import orm,db
import uuid
import datetime
import time

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
    checkbookList = UserCheckbookMap.find_by("where user_id=%s",u.id)
    if not checkbookList:
        checkbookList=[]
    return checkbookList