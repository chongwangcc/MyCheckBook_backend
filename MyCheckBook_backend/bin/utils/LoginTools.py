# -*- coding: UTF-8 -*-
from models.Models import UserInfo,AuthCode
from utils import orm,db
from utils import zaTools
import datetime
import time


def checkPassword(user_name,password):
    """
    检查用户名密码是否正确
    :param user_name:
    :param password:
    :return:
    """
    u = UserInfo.find_by("where name = ? and password = ?", user_name,password);
    if u:
        return True
    else:
        return False


def checkAuthCode(user_name,auth):
    """
    检查authcode有没有过期
    :param user_name:
    :param auth:
    :return:
    """
    u = UserInfo.find_first("where name = ?", user_name);
    if not u:
        return False
    auth = AuthCode.find_first("where auth_code = ? and user_id = ?",auth,u.id)
    if not auth:
        return False
    time_now = int(time.mktime(datetime.datetime.now().timetuple()))
    if int(auth.endDate)<time_now:
        return False
    return True


def genAuthCode(user_name,days=30):
    """
    生成授权码，默认30天内有效
    :param user_name:
    :param days:
    :return:
    """
    #1.判断User是否存在
    u = UserInfo.find_first("where name = ?", user_name);
    if not u:
        return None

    #2.构造Auth对象
    auth_code_id = zaTools.genID()
    time_now = datetime.datetime.now()
    time_end=time_now+datetime.timedelta(days=days)
    dataLong=int(time.mktime(time_end.timetuple()))
    print(dataLong)
    permission=1
    auth = AuthCode(auth_code=auth_code_id,user_id=u.id,endDate=dataLong,permission=1)

    #3.保存到数据库
    auth.insert()

    #4.返回
    return auth.auth_code



def initUser():
    """
    初始化cc ,mm的默认账户
    :return:
    """
    u = UserInfo(id=zaTools.genID(),name="cc",password="lovemiao",description="cc的个人账号")
    u.insert()
    u = UserInfo(id=zaTools.genID(), name="mm", password="lovechong", description="mm的个人账号")
    u.insert();
    pass


if __name__ == "__main__":
    db.create_engine(user='root', password='pwd123456', database='checkbook', host="139.129.230.162", port=3400)
    genAuthCode("cc")