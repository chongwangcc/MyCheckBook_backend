from flask import Flask , request,jsonify

app = Flask(__name__)
version = "v1.0"

"""
登陆接口
"""


@app.route('/checkbook/api/'+version+'/login', methods=['GET'])
def login():
    return 'login!'

"""
#######################操作checkbook 接口#############################
"""

@app.route('/checkbook/api/'+version+'/checkbooks', methods=['GET'])
def get_checkbooks_list():
    user_name=request.args.get('user_name')
    auth_code = request.args.get('auth_code')

    return 'checkbooks' + user_name+auth_code


@app.route('/checkbook/api/'+version+'/checkbooks', methods=['POST'])
def add_checkbook():
    user_name=request.args.get('user_name')
    auth_code = request.args.get('auth_code')
    isModify = request.args.get('isModify')
    checkbook = request.args.get('checkbook')

    return 'checkbooks' + user_name+auth_code


@app.route('/checkbook/api/'+version+'/checkbooks', methods=['DELETE'])
def delete_checkbook():
    user_name=request.args.get('user_name')
    auth_code = request.args.get('auth_code')
    checkbook_id = request.args.get('checkbook_id')

    return 'checkbooks' + user_name+auth_code


@app.route('/checkbook/api/'+version+'/checkbook/info', methods=['GET'])
def get_checkbook_info():
    user_name=request.args.get('user_name')
    auth_code = request.args.get('auth_code')
    checkbook_id = request.args.get('checkbook_id')

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
    app.run(host='0.0.0.0', port=9080, debug=True)