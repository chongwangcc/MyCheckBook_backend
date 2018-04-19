# -*- coding: UTF-8 -*-
from flask import Flask , request,jsonify
from utils import LoginTools, CheckbookTools
from models import  ReturnEntity

import json
app = Flask(__name__)
version = "v1.0"
restful_port = 9080
from utils import orm,db

db.create_engine(user='root', password='pwd123456', database='checkbook',host="139.129.230.162", port=3400)

"""
登陆接口
"""


@app.route('/checkbook/api/'+version+'/login', methods=['GET'])
def login():
    """
    用户名密码登陆
    :return:
    """
    user_name = request.args.get('user_name')
    password = request.args.get('password')
    b = LoginTools.checkPassword(user_name,password)

    status = ReturnEntity.ReturnStatus()
    data = ReturnEntity.LoginReturn()
    returnvalue = ReturnEntity.ReturnEntity()
    returnvalue.status=status

    code = LoginTools.genAuthCode(user_name)
    if b and code:
        status.code = 0
        status.msg = u"成功"
        data.auth_code=code
        returnvalue.data = data
    else:
        status.code = 10500
        status.msg = u"登陆失败，用户名或密码错误"

        pass

    return json.dumps(returnvalue,ensure_ascii=False,default=ReturnEntity.convert_to_builtin_type)


"""
#######################操作checkbook 接口#############################
"""


@app.route('/checkbook/api/'+version+'/checkbooks', methods=['GET'])
def get_checkbooks_list():
    """
    获得记帐本列表
    :return:
    """
    user_name=request.args.get('user_name')
    auth_code = request.args.get('auth_code')
    #1. 准备返回值
    status = ReturnEntity.ReturnStatus()
    data = ReturnEntity.CheckbookListReturn()
    returnvalue = ReturnEntity.ReturnEntity()
    returnvalue.status = status
    #2. 获得checkbooks
    b = LoginTools.checkAuthCode(user_name, auth_code)
    checkbooks = CheckbookTools.getCheckbookListByUser(user_name)
    if b and checkbooks:
        status.code = 0
        status.msg = u"成功"
        returnvalue.data=data
        data.checkbooks=checkbooks
    else:
        status.code = 10500
        status.msg = u"获取记账本失败"
    return json.dumps(returnvalue,ensure_ascii=False,default=ReturnEntity.convert_to_builtin_type)


@app.route('/checkbook/api/'+version+'/checkbooks', methods=['POST'])
def add_checkbook():
    """
    添加一个记账本
    :return:
    """
    user_name=request.args.get('user_name')
    auth_code = request.args.get('auth_code')
    checkbook_json = request.get_json()
    #1.准备返回值
    status = ReturnEntity.ReturnStatus()
    data = ReturnEntity.CheckbookAddReturn()
    returnvalue = ReturnEntity.ReturnEntity()
    returnvalue.status = status
    #2.调用接口
    b = LoginTools.checkAuthCode(user_name, auth_code)
    if b:
        checkbook_id = CheckbookTools.addCheckbook(user_name, checkbook_json)
        status.code = 0
        status.msg = u"成功"
        data.checkbook_id = checkbook_id
        returnvalue.data = data
    else:
        status.code = 10500
        status.msg = u"失败"
    return json.dumps(returnvalue,ensure_ascii=False,default=ReturnEntity.convert_to_builtin_type)


@app.route('/checkbook/api/'+version+'/checkbooks', methods=['DELETE'])
def delete_checkbook():
    user_name=request.args.get('user_name')
    auth_code = request.args.get('auth_code')
    checkbook_id = request.args.get('checkbook_id')
    # 1.准备返回值
    status = ReturnEntity.ReturnStatus()
    data = ReturnEntity.CheckbookAddReturn()
    returnvalue = ReturnEntity.ReturnEntity()
    returnvalue.status = status
    #2.验证登陆效果
    b = LoginTools.checkAuthCode(user_name, auth_code)
    if b:
        CheckbookTools.deleteCheckbook(checkbook_id)
    data.checkbook_id=checkbook_id
    status.code=0
    status.msg="成功"
    return json.dumps(returnvalue,ensure_ascii=False,default=ReturnEntity.convert_to_builtin_type)


@app.route('/checkbook/api/'+version+'/checkbook/info', methods=['GET'])
def get_checkbook_info():
    user_name=request.args.get('user_name')
    auth_code = request.args.get('auth_code')
    checkbook_id = request.args.get('checkbook_id')
    #1.准备返回值
    status = ReturnEntity.ReturnStatus()
    data = ReturnEntity.CheckbookAddReturn()
    returnvalue = ReturnEntity.ReturnEntity()
    returnvalue.status = status
    #
    return 'checkbooks' + user_name+auth_code


@app.route('/checkbook/api/'+version+'/checkbook/invitation', methods=['GET'])
def join_checkbook_by_invitation():
    user_name=request.args.get('user_name')
    auth_code = request.args.get('auth_code')
    invitation_code = request.args.get('invitation_code')

    return 'checkbooks' + user_name+auth_code


@app.route('/checkbook/api/'+version+'/checkbook/invitation', methods=['POST'])
def makeup_checkbook_invitation():
    user_name=request.args.get('user_name')
    auth_code = request.args.get('auth_code')
    checkbook_id = request.args.get('checkbook_id')
    nums = request.args.get('nums')
    permission = request.args.get('permission')

    return 'checkbooks' + user_name+auth_code


"""
#######################操作account 账户细数据 接口#############################
"""


@app.route('/checkbook/api/'+version+'/account', methods=['GET'])
def get_accounts_list():
    user_name=request.args.get('user_name')
    auth_code = request.args.get('auth_code')
    checkbook_id = request.args.get('checkbook_id')

    return 'checkbooks' + user_name+auth_code


@app.route('/checkbook/api/'+version+'/account/info', methods=['GET'])
def get_account_info():
    user_name=request.args.get('user_name')
    auth_code = request.args.get('auth_code')
    account_id = request.args.get('account_id')

    return 'checkbooks' + user_name+auth_code


@app.route('/checkbook/api/'+version+'/account', methods=['DELETE'])
def delete_account():
    user_name=request.args.get('user_name')
    auth_code = request.args.get('auth_code')
    account_id = request.args.get('account_id')

    return 'checkbooks' + user_name+auth_code


@app.route('/checkbook/api/'+version+'/account', methods=['POST'])
def add_account():
    user_name=request.args.get('user_name')
    auth_code = request.args.get('auth_code')
    account_id = request.args.get('account')
    is_modify = request.args.get('isModify')

    return 'checkbooks' + user_name+auth_code


"""
#######################操作account 账户细数据 接口#############################
"""


@app.route('/checkbook/api/'+version+'/details', methods=['GET'])
def get_details_list():
    user_name=request.args.get('user_name')
    auth_code = request.args.get('auth_code')
    checkbook_id = request.args.get('checkbook_id')
    month = request.args.get('month')

    return 'checkbooks' + user_name+auth_code


@app.route('/checkbook/api/'+version+'/detail', methods=['GET'])
def get_details_info():
    user_name=request.args.get('user_name')
    auth_code = request.args.get('auth_code')
    detail_id = request.args.get('detail_id')

    return 'checkbooks' + user_name+auth_code


@app.route('/checkbook/api/'+version+'/detail', methods=['DELETE'])
def delete_detail():
    user_name=request.args.get('user_name')
    auth_code = request.args.get('auth_code')
    detail_id = request.args.get('detail_id')

    return 'checkbooks' + user_name+auth_code


@app.route('/checkbook/api/'+version+'/detail', methods=['POST'])
def add_detail():
    user_name=request.args.get('user_name')
    auth_code = request.args.get('auth_code')
    detail_id = request.args.get('detail')
    is_modify = request.args.get('isModify')

    return 'checkbooks' + user_name+auth_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=restful_port, debug=True)