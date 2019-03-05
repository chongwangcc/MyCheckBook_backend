#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/3/5 11:02 
# @Author : wangchong 
# @Email: chongwangcc@gmail.com
# @File : restful_v2.py
# @Software: PyCharm


from flask_login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)
from flask import Flask, render_template, jsonify, request, redirect
from flask_restful import Api, Resource,reqparse

from tools.app import app

api = Api(app)


class DetailsAPI(Resource):
    """
    记账本明细 的操作API
    """
    def get(self, id):
        pass

    def put(self, id):
        pass

    def post(self):
        pass

    def delete(self, id):
        pass


class CheckbookAPI(Resource):
    """
    对记账本 操作 的API
    """

    def get(self, id):
        pass

    def put(self, id):
        pass

    def post(self):
        pass

    def delete(self, id):
        pass


class ReportAPI(Resource):
    """
    对财报操作 的API
    """
    def get(self, id):
        pass

    def put(self, id):
        pass

    def post(self):
        pass

    def delete(self, id):
        pass


class BudgetAPI(Resource):
    """
    对预算操作的 API
    """
    def get(self, id):
        pass

    def put(self, id):
        pass

    def post(self):
        pass

    def delete(self, id):
        pass


class UserAPI(Resource):
    """
    对用户操作的API
    """
    def get(self, id):
        pass

    def put(self, id):
        pass

    def post(self):
        pass

    def delete(self, id):
        pass


class TrendsAPI(Resource):
    """
    趋势走势图 的获得API
    """
    get_parser = reqparse.RequestParser()
    get_parser.add_argument('month_nums', type=int, location='args', required=True)

    def get(self, checkbook_id):
        print(checkbook_id)
        args = TrendsAPI.get_parser.parse_args()
        id = args.get('month_nums')
        print(id)
        pass


api.add_resource(TrendsAPI, '/api/v1/trends/all/<checkbook_id>', endpoint='trends')

# @app.route("/api/v1/trends/all/<checkbook_id>?month_nums=12", methods=["GET"])
# @login_required
# def weekly_statistics1(checkbook_id):
#     """
#     获得每周相关的统计信息、每周概览的统计信息从这个一个API调用
#     :param date_str:
#     :return:
#     """
#     # 1.构造缓存查询任务
#     result = {}
#
#     # 3. 构造返回JSON
#     return jsonify(result)