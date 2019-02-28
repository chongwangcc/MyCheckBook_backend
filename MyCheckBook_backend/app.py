#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/2/25 5:40 
# @Author : wangchong 
# @Email: chongwangcc@gmail.com
# @File : app.py
# @Software: PyCharm

from flask import Flask, render_template, jsonify, request, redirect
from flask_login.login_manager import LoginManager
from flask_login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)


app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_name):
    return SqlTools.fetch_user_info(user_name)


@app.route("/login", methods=['GET', 'POST'])
def login():
    """
    打开默认界面
    :return:
    """
    if request.method == 'POST':
        user_name = request.form["username"]
        password = request.form["password"]
        # 判断用户密码是否正确
        m_user = SqlTools.fetch_user_info(user_name)
        if m_user is not None and m_user.password == password:
            # 登陆成功
            login_user(m_user, remember=True)
            # 跳转
            return redirect("/weeksum")
        else:
            # 登陆失败，弹出消息框
            return render_template('login.html')

    # 判断有没有用户登录
    return render_template('login.html')


@app.route("/logout", methods=["POST","GET"])
@login_required
def logout():
    """
    登出界面
    :return:
    """
    logout_user()
    return redirect('/login')


@app.errorhandler(404)
def page_not_found(e):
    """
    找不到界面的默认返回页
    :param e:
    :return:
    """
    return render_template('404.html'), 40