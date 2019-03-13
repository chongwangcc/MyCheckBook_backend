#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/2/25 5:40 
# @Author : wangchong 
# @Email: chongwangcc@gmail.com
# @File : app.py
# @Software: PyCharm

from flask import Flask, render_template, jsonify, request, redirect
from flask_login.login_manager import LoginManager

from tools.SqlTools import *


app = Flask(__name__, static_folder='../static', template_folder="../templates")
app.config['SECRET_KEY'] = '123456'
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_name):
    return UserTools.fetch_user_info(user_name)
