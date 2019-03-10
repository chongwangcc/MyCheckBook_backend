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
from random import choice

api = Api(app)


class DetailsListAPI(Resource):
    """
    按照记账本，月份，获得所有明细
    """

    def __init__(self):
        self.get_parser = reqparse.RequestParser()
        self.get_parser.add_argument('checkbook_id', type=str, location='args', required=True)
        self.get_parser.add_argument('month_str', type=str, location='args', required=True)
        self.get_parser.add_argument('lite', type=str, location='args', required=False, default=False)
        self.get_parser.add_argument('category', type=str, location='args', required=False, default=None)
        self.get_parser.add_argument('type', type=str, location='args', required=False, default=None)
        self.get_parser.add_argument('account_name', type=str, location='args', required=False, default=None)
        self.get_parser.add_argument('seconds_account_name', type=str, location='args', required=False, default=None)
        self.get_parser.add_argument('seconds_account_name', type=str, location='args', required=False, default=None)
        self.get_parser.add_argument('page', type=int, location='args', required=False, default=1)
        self.get_parser.add_argument('limit', type=int, location='args', required=False, default=10)
        self.all_details = []
        self.all_details_lite = []

        for i in range(0,100):
            t_details={}
            t_details["date"] = "2019.2.28"
            t_details["category"] = choice(["零食", "社交","餐饮","住房","医疗","工资"])
            t_details["money"] = choice([12,13,59,100,400])
            t_details["remark"] = choice(["买酸奶", "交话费","海贼王","仙剑4","随便吧","DMCC"])
            t_details["isCash"] = choice(["现金", "信用卡"])
            t_details["type"] = choice(["收入", "支出", "流入", "流出"])
            t_details["checkbook_name"] = "CM家庭记账本"
            t_details["account_name"] = choice(["花销账户","投资账户","储蓄账户"])
            t_details["seconds_account_name"] = choice(["生活费账户", "doodads账户","教育账户","风险备付金","住房基金"])
            t_details["updater"] = choice(["MM","CC"])

            self.all_details.append(t_details)
        pass

    def get(self):
        args = self.get_parser.parse_args()
        checkbook_id = args.get('checkbook_id')
        month_str = args.get('month_str')
        lite = args.get('lite')
        account_name = args.get('account_name')
        type = args.get('type')
        category = args.get('category')
        account_name = args.get('account_name')
        seconds_account_name = args.get('seconds_account_name')
        data = self.all_details
        if category is not  None:
            data = self.all_details[0:5]
        if account_name is not None:
            data = self.all_details[0:10]




        result={
            "code":0,
            "msg":"",
            "count":len(data),
            "data":data
        }

        return jsonify(result)

        pass


class DetailsSumAPI(Resource):
    """
    获得记账本的统计信息
    """
    def __init__(self):
        self.get_parser = reqparse.RequestParser()
        self.get_parser.add_argument('checkbook_id', type=str, location='args', required=True)
        self.get_parser.add_argument('month_str', type=str, location='args', required=True)
        self.all_details = []
        self.all_details_lite = []

        for i in range(0,100):
            t_details={}
            t_details["date"] = "2019.2.28"
            t_details["category"] = choice(["零食", "社交","餐饮","住房","医疗","工资"])
            t_details["money"] = choice([12,13,59,100,400])
            t_details["remark"] = choice(["买酸奶", "交话费","海贼王","仙剑4","随便吧","DMCC"])
            t_details["isCash"] = choice(["现金", "信用卡"])
            t_details["type"] = choice(["收入", "支出", "流入", "流出"])
            t_details["checkbook_name"] = "CM家庭记账本"
            t_details["account_name"] = choice(["花销账户","投资账户","储蓄账户"])
            t_details["seconds_account_name"] = choice(["生活费账户", "doodads账户","教育账户","风险备付金","住房基金"])
            t_details["updater"] = choice(["MM","CC"])

            self.all_details.append(t_details)
        pass

    def get(self):
        result={}
        result["income_category"] = {
            "legend":["生活费", "零食", "购物", "运动", "娱乐"],
            "sumType":"总收入",
            "sumValue":200,
            "data":[{
                "value": 3661,
                "name": '生活费'
            }, {
                "value": 5713,
                "name": '零食'
            }, {
                "value": 9938,
                "name": '购物'
            }, {
                "value": 17623,
                "name": '运动'
            }, {
                "value": 3299,
                "name": '娱乐'
            }]
        }
        result["income_account"] = {
            "legend":["投资账户", "花销账户", "储蓄账户", "生活费账户", "doodads账户", "风险备付金", "住房账户","教育基金"],
            "sumType":"总收入",
            "sumValue":200,
            "data1": [{
                "value": 3661,
                "name": '投资账户'
            }, {
                "value": 5713,
                "name": '花销账户'
            }, {
                "value": 9938,
                "name": '储蓄账户'
            }],
            "data2": [{
                "value": 3661,
                "name": 'doodads账户'
            }, {
                "value": 5713,
                "name": '生活费账户'
            }, {
                "value": 9938,
                "name": '风险备付金'
            }, {
                "value": 9938,
                "name": '住房账户'
            }, {
                "value": 9938,
                "name": '教育基金'
            }, {
                "value": 9938,
                "name": '投资-现金'
            }, {
                "value": 9938,
                "name": '投资股票'
            }, {
                "value": 9938,
                "name": '储蓄现金'
            }, {
                "value": 9938,
                "name": '储蓄烂账'
            }]
        }
        result["spent_category"] = {
            "legend":["生活费", "零食", "购物", "运动", "娱乐"],
            "sumType":"总支出",
            "sumValue":200,
            "data":[{
                "value": 3661,
                "name": '生活费'
            }, {
                "value": 5713,
                "name": '零食'
            }, {
                "value": 9938,
                "name": '购物'
            }, {
                "value": 17623,
                "name": '运动'
            }, {
                "value": 3299,
                "name": '娱乐'
            }]
        }
        result["spent_account"] = {
            "legend":["投资账户", "花销账户", "储蓄账户", "生活费账户", "doodads账户", "风险备付金", "住房账户","教育基金"],
            "sumType":"总支出",
            "sumValue":200,
            "data1": [{
                "value": 3661,
                "name": '投资账户'
            }, {
                "value": 5713,
                "name": '花销账户'
            }, {
                "value": 9938,
                "name": '储蓄账户'
            }],
            "data2": [{
                "value": 3661,
                "name": 'doodads账户'
            }, {
                "value": 5713,
                "name": '生活费账户'
            }, {
                "value": 9938,
                "name": '风险备付金'
            }, {
                "value": 9938,
                "name": '住房账户'
            }, {
                "value": 9938,
                "name": '教育基金'
            }, {
                "value": 9938,
                "name": '投资-现金'
            }, {
                "value": 9938,
                "name": '投资股票'
            }, {
                "value": 9938,
                "name": '储蓄现金'
            }, {
                "value": 9938,
                "name": '储蓄烂账'
            }]
        }
        result["inflow_category"] = {
            "legend":["生活费", "零食", "购物", "运动", "娱乐"],
            "sumType":"总流入",
            "sumValue":200,
            "data":[{
                "value": 3661,
                "name": '生活费'
            }, {
                "value": 5713,
                "name": '零食'
            }, {
                "value": 9938,
                "name": '购物'
            }, {
                "value": 17623,
                "name": '运动'
            }, {
                "value": 3299,
                "name": '娱乐'
            }]
        }
        result["inflow_account"] = {
            "legend":["投资账户", "花销账户", "储蓄账户", "生活费账户", "doodads账户", "风险备付金", "住房账户","教育基金"],
            "sumType":"总流入",
            "sumValue":200,
            "data1": [{
                "value": 3661,
                "name": '投资账户'
            }, {
                "value": 5713,
                "name": '花销账户'
            }, {
                "value": 9938,
                "name": '储蓄账户'
            }],
            "data2": [{
                "value": 3661,
                "name": 'doodads账户'
            }, {
                "value": 5713,
                "name": '生活费账户'
            }, {
                "value": 9938,
                "name": '风险备付金'
            }, {
                "value": 9938,
                "name": '住房账户'
            }, {
                "value": 9938,
                "name": '教育基金'
            }, {
                "value": 9938,
                "name": '投资-现金'
            }, {
                "value": 9938,
                "name": '投资股票'
            }, {
                "value": 9938,
                "name": '储蓄现金'
            }, {
                "value": 9938,
                "name": '储蓄烂账'
            }]
        }
        result["outflow_category"] = {
            "legend":["生活费", "零食", "购物", "运动", "娱乐"],
            "sumType":"总流出",
            "sumValue":200,
            "data":[{
                "value": 3661,
                "name": '生活费'
            }, {
                "value": 5713,
                "name": '零食'
            }, {
                "value": 9938,
                "name": '购物'
            }, {
                "value": 17623,
                "name": '运动'
            }, {
                "value": 3299,
                "name": '娱乐'
            }]
        }
        result["outflow_account"] = {
            "legend":["投资账户", "花销账户", "储蓄账户", "生活费账户", "doodads账户", "风险备付金", "住房账户","教育基金"],
            "sumType":"总流出",
            "sumValue":200,
            "data1": [{
                "value": 3661,
                "name": '投资账户'
            }, {
                "value": 5713,
                "name": '花销账户'
            }, {
                "value": 9938,
                "name": '储蓄账户'
            }],
            "data2": [{
                "value": 3661,
                "name": 'doodads账户'
            }, {
                "value": 5713,
                "name": '生活费账户'
            }, {
                "value": 9938,
                "name": '风险备付金'
            }, {
                "value": 9938,
                "name": '住房账户'
            }, {
                "value": 9938,
                "name": '教育基金'
            }, {
                "value": 9938,
                "name": '投资-现金'
            }, {
                "value": 9938,
                "name": '投资股票'
            }, {
                "value": 9938,
                "name": '储蓄现金'
            }, {
                "value": 9938,
                "name": '储蓄烂账'
            }]
        }
        return jsonify(result)

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
    checkbook_list = [
        {
            "checkbook_id": "1",
            "checkbook_name": "CM家庭记账本",
            "create_time": "2018-01-02 12:20:40",
            "last_update_time": "2018-01-02 12:45:23",
            "description": "CM家庭记账本，计算家庭收支情况",
            "partner": "cc, mm",
            "my_role": "创建者",
            "my_permission": "读、写、邀请",
            "status": "正常",
            "rules": "子账户：消费、投资、储蓄：7：2：1",
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
    def get(self):

        result={
            "code":0,
            "msg":"",
            "count":len(self.checkbook_list),
            "data":self.checkbook_list,
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
        for value in CheckbookListAPI.checkbook_list:
            if value["checkbook_id"] == checkbook_id:
                return jsonify(value)

        return jsonify({})

    def put(self, checkbook_id):
        pass

    def post(self):
        # 添加一个记账本
        get_parser = reqparse.RequestParser()
        get_parser.add_argument('name', type=str,  required=False)
        get_parser.add_argument('description', type=str,  required=False)
        get_parser.add_argument('owner', type=str,  required=False)
        args = get_parser.parse_args()
        print(args)
        return jsonify({})

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
api.add_resource(CheckbookAPI, '/api/v1/checkbook', endpoint='checkbook')
api.add_resource(CheckbookInvitationCodeAPI, '/api/v1/CheckbookInvitationCode', endpoint='CheckbookInvitationCode')
api.add_resource(DetailsListAPI, '/api/v1/details', endpoint='details')
api.add_resource(DetailsSumAPI, '/api/v1/detailsum', endpoint='detailsum')

