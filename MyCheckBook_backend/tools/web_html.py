#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/3/5 11:03 
# @Author : wangchong 
# @Email: chongwangcc@gmail.com
# @File : web_html.py 
# @Software: PyCharm
from flask import Flask, render_template, jsonify, request, redirect
from flask_login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)
from tools.app import app
from tools import SqlTools

@app.route("/", methods=["GET"])
@login_required
def index():
    """
    打开首页
    :return:
    """
    return render_template('./index/index.html')


@app.route("/overview", methods=["GET"])
@login_required
def overview():
    """
    查看概览
    :return:
    """
    return render_template('./index/overview.html')


@app.route("/checkbook_manage", methods=["GET"])
@login_required
def checkbook_manage():
    """
    记账本管理界面
    :return:
    """
    return render_template('./index/checkbook_manage.html')


@app.route("/detail_manage", methods=["GET"])
@login_required
def detail_manage():
    """
    明细挂了你界面
    :return:
    """
    return render_template('./index/detail_manage.html')


@app.route("/asset_manage", methods=["GET"])
@login_required
def asset_manage():
    """
    资产负债管理界面
    :return:
    """
    return render_template('./index/asset_manage.html')


@app.route("/report_manage", methods=["GET"])
@login_required
def report_manage():
    """
    财报管理界面
    :return:
    """
    return render_template('./index/report_manage.html')


@app.route("/budget_manage", methods=["GET"])
@login_required
def budget_manage():
    """
    预算管理界面
    :return:
    """
    return render_template('./index/budget_manage.html')


@app.route("/invest_manage", methods=["GET"])
@login_required
def invest_manage():
    """
    投资管理界面
    :return:
    """
    return render_template('./index/invest_manage.html')


@app.route("/trends_img", methods=["GET"])
@login_required
def trends_img():
    """
    走势图 界面
    :return:
    """
    return render_template('./index/trends_img.html')



@app.route("/login", methods=['GET', 'POST'])
def login():
    """
    登陆界面
    :return:
    """
    if request.method == 'POST':
        try:
            user_name = request.form["username"]
            password = request.form["password"]
            # 判断用户密码是否正确
            m_user = SqlTools.fetch_user_info(user_name)
            if m_user is not None and m_user.password == password:
                # 登陆成功
                login_user(m_user, remember=True)
                # 跳转
                return redirect("/")
            else:
                # 登陆失败，弹出消息框
                return render_template('./index/login.html')
        except:
            pass

    # 判断有没有用户登录
    return render_template('./index/login.html')


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
    return render_template('./index/404.html'), 40

