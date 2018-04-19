# -*- coding: UTF-8 -*-
from models.Models import UserCheckbookMap,UserInfo,DetailsInfo

from utils import zaTools


def addDetails(user_name,detail_json):
    """
    添加一条明细
    :param checkbook_id:
    :param detail_json:
    :return:
    """
    id = detail_json.get("id", zaTools.genID())
    checkbook_id = detail_json.get("checkbook_id", "")
    account_id = detail_json.get("account_id", "")
    last_update_user_name = detail_json.get("last_update_user_name", 1)
    date_str = detail_json.get("date_str", "")
    year,month,day = date_str.split("-")
    money = detail_json.get("money", 0)
    description = detail_json.get("description", 0)
    balanceType = detail_json.get("balance_type", 0)
    Category = detail_json.get("category_type", 0)
    isCreditcard = detail_json.get("is_creditCard", 0)
    updateTime = detail_json.get("update_time", 0)
    createTime = detail_json.get("create_time", 0)
    version = detail_json.get("version",1)
    handprint = detail_json.get("handprint",1)

    u = UserInfo.find_first("where name = ?", last_update_user_name);
    dInfo_new = DetailsInfo(id=id,
                checkbook_id=checkbook_id,
                account_id=account_id,
                last_update_user_id=u.id,
                date_str=date_str,
                year=year,
                month=month,
                day=day,
                money=money,
                description=description,
                balanceType=balanceType,
                Category=Category,
                isCreditcard=isCreditcard,
                updateTime=updateTime,
                createTime=createTime)
    dInfo_old = DetailsInfo.find_first("where id=?",id)
    #1.比较要插入的，和数据库中存在的
    b = compareDetails(dInfo_old,dInfo_new)
    if b:
        #插入到数据库中
        try:
            dInfo_new.insert()
        except Exception as e:
            print(e)
            dInfo_new.update()
        pass
    return dInfo_new

def deleteDetail(user_name,detail_id):
    """
    删除一条明细
    :param user_name:
    :param detail_id:
    :return:
    """
    #1.读出来明细
    detail = getDetailInfo(detail_id)
    if not detail:
        return True
    #2.读出明细对应的记账本
    ucMap = UserCheckbookMap.find_first("where user_id=? and checkbook_id=? and permission>0 ", u.id, checkbook_id)
    #3. 判断记账本id有没有user_name
    if not ucMap:
        return False
    detail.delete()
    return True

def getDetailInfo(detail_id):
    """
    获得一条明细的名字
    :param detail_id:
    :return:
    """
    detail=DetailsInfo.find_first("where id=?",detail_id)
    return detail


def compareDetails(details_old,detail_new):
    """
    比较两个明细记录，哪个更新一些
    :param details_old:
    :param detail_new:
    :return:
    """
    #TODO
    return  True