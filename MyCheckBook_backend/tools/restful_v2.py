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


class CheckbookListAPI(Resource):
    """
    获得记账本列表
    """
    def get(self):
        checkbook_list=[
            {
                "checkbook_id": "1",
                "checkbook_name": "CM家庭记账本",
                "create_time": "2018-01-02 12:20:40",
                "last_update_time": "2018-01-02 12:45:23",
                "description": "CM家庭记账本，计算家庭收支情况",
                "partner": "cc, mm",
                "my_role": "创建者",
                "my_permission":"读、写、邀请",
                "status":"正常",
                "rules":"子账户：消费、投资、储蓄：7：2：1",
            },
            {
                "checkbook_id": "2",
                "checkbook_name": "CM工作室记账本",
                "create_time": "2018-01-02 12:20:40",
                "last_update_time": "2018-01-02 12:45:23",
                "description": "CM家庭记账本，计算家庭收支情况",
                "partner": "cc, mm",
                "my_role": "创建者",
                "my_permission": "读、写、邀请",
                "status": "正常",
                "rules": "子账户：消费、投资、储蓄：7：2：1",
            }
        ]
        result={
            "code":0,
            "msg":"",
            "count":len(checkbook_list),
            "data":checkbook_list,
        }

        return jsonify(result)


class CheckbookInvitationCodeAPI(Resource):
    """
    记账本邀请码的使用
    """
    decorators = [login_required]
    get_parser = reqparse.RequestParser()
    get_parser.add_argument('checkbook_id', type=str, location='args', required=True, default=12)
    invateMap={}

    code_parser = reqparse.RequestParser()
    code_parser.add_argument('code', type=str, location='args', required=True, default=12)


    def get(self):
        args = CheckbookInvitationCodeAPI.get_parser.parse_args()
        checkbook_id = args.get('checkbook_id')
        # 生成邀请码
        invationCode="fdasjkljkn"
        CheckbookInvitationCodeAPI.invateMap[invationCode]={
            "checkbook_id":checkbook_id,
            "creator":current_user.id
        };
        print(CheckbookInvitationCodeAPI.invateMap)
        return jsonify({"invationCode":invationCode})


    def post(self):
        # 使用邀请码加入记账组
        try:
            args = CheckbookInvitationCodeAPI.code_parser.parse_args()
            code = args.get('code')
            print(code)
            checkbook_id = CheckbookInvitationCodeAPI.invateMap.get(code)

            print(checkbook_id)
            if checkbook_id is None:
                raise Exception("error id")

            return jsonify({"checkbook_id":checkbook_id})
        except:
            pass
        return jsonify({"error":"ered"})



class CheckbookAPI(Resource):
    """
    对记账本 操作 的API
    """

    def get(self, checkbook_id):
        pass

    def put(self, checkbook_id):
        pass

    def post(self):
        pass

    def delete(self, checkbook_id):
        print(checkbook_id)
        return jsonify({}),500
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
    # 添加认证信息
    decorators = [login_required]

    # url参数解析器
    get_parser = reqparse.RequestParser()
    get_parser.add_argument('month_nums', type=int, location='args', required=False, default=12)

    def get(self, checkbook_id):
        args = TrendsAPI.get_parser.parse_args()
        month_nums  = args.get('month_nums')
        # TODO 根据记账本 和 月份数， 获得所有的相关数据
        print(checkbook_id)
        print(month_nums)
        # 构造需要的数据，返回
        result = {}
        result["remain_income_trends"] = {
            "xAxis": ["2019-01", "2019-02", "2019-03", "2019-04", "2019-05", "2019-06", "2019-07"],
            "profit": [10, 12, 21, 54, 260, 830, -710],
            "cashflow": [30, 182, 434, 791, 390, 30, 10]
        }
        result["income_category_trends"] = {
            "title":"收入趋势图",
            "legend":["工资","S象限","投资收入"],
            "xAxis": ["2019-01", "2019-02", "2019-03", "2019-04", "2019-05", "2019-06", "2019-07"],
            "all_datas":[
                {"name":"工资",
                 "data":[120, 132, 101, 134, 90, 230, 210]
                 },
                {"name":"S象限",
                 "data":[120, 132, 101, 134, 90, 230, 210]
                 },
                {"name":"投资收入",
                 "data":[120, 132, 101, 134, 90, 230, 210]
                 }
            ]
        }
        result["spent_category_trends"] = {
            "title":"支出趋势图",
            "legend":["生活费","doodads","教育"],
            "xAxis": ["2019-01", "2019-02", "2019-03", "2019-04", "2019-05", "2019-06", "2019-07"],
            "all_datas":[
                {"name":"生活费",
                 "data":[120, 132, 101, 134, 90, 230, 210]
                 },
                {"name":"doodads",
                 "data":[120, 132, 101, 134, 90, 230, 210]
                 },
                {"name":"教育",
                 "data":[120, 132, 101, 134, 90, 230, 210]
                 }
            ]
        }
        result["inflow_category_trends"] = {
            "title":"流入趋势图",
            "legend":["工资","S象限","投资收入"],
            "xAxis": ["2019-01", "2019-02", "2019-03", "2019-04", "2019-05", "2019-06", "2019-07"],
            "all_datas":[
                {"name":"工资",
                 "data":[120, 132, 101, 134, 90, 230, 210]
                 },
                {"name":"S象限",
                 "data":[120, 132, 101, 134, 90, 230, 210]
                 },
                {"name":"投资收入",
                 "data":[120, 132, 101, 134, 90, 230, 210]
                 }
            ]
        }
        result["outflow_category_trends"] = {
            "title":"流出趋势图",
            "legend":["生活费","doodads","教育"],
            "xAxis": ["2019-01", "2019-02", "2019-03", "2019-04", "2019-05", "2019-06", "2019-07"],
            "all_datas":[
                {"name":"生活费",
                 "data":[120, 132, 101, 134, 90, 230, 210]
                 },
                {"name":"doodads",
                 "data":[120, 132, 101, 134, 90, 230, 210]
                 },
                {"name":"教育",
                 "data":[120, 132, 101, 134, 90, 230, 210]
                 }
            ]
        }
        result["asset_category_trends"] = {
            "title":"资产趋势图",
            "legend":["现金","货币基金","投资资产"],
            "xAxis": ["2019-01", "2019-02", "2019-03", "2019-04", "2019-05", "2019-06", "2019-07"],
            "all_datas":[
                {"name":"现金",
                 "data":[120, 132, 101, 134, 90, 230, 210]
                 },
                {"name":"货币基金",
                 "data":[120, 132, 101, 134, 90, 230, 210]
                 },
                {"name":"投资资产",
                 "data":[120, 132, 101, 134, 90, 230, 210]
                 }
            ]
        }
        result["liability_category_trends"] = {
            "title":"负债趋势图",
            "legend":["短期负债","长期负债"],
            "xAxis": ["2019-01", "2019-02", "2019-03", "2019-04", "2019-05", "2019-06", "2019-07"],
            "all_datas":[
                {"name":"短期负债",
                 "data":[120, 132, 101, 134, 90, 230, 210]
                 },
                {"name":"长期负债",
                 "data":[120, 132, 101, 134, 90, 230, 210]
                 },
            ]
        }


        return jsonify(result)


api.add_resource(TrendsAPI, '/api/v1/trends/checkbooks/<checkbook_id>', endpoint='trends')
api.add_resource(CheckbookListAPI, "/api/v1/checkbooks", endpoint="checkbookList")
api.add_resource(CheckbookAPI, '/api/v1/checkbooks/<checkbook_id>', endpoint='checkbook')
api.add_resource(CheckbookInvitationCodeAPI, '/api/v1/CheckbookInvitationCode', endpoint='CheckbookInvitationCode')

