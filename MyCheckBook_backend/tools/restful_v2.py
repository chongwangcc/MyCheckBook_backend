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
import json
from datetime import datetime
from random import choice

from tools.app import app
from tools.SqlTools import *
from tools.utils import id_generator


api = Api(app)


class CheckbookListAPI(Resource):
    """
    获得记账本列表
    """
    decorators = [login_required]

    def get(self):
        #  获得用户名下所有的记账本
        checkbooks = fetch_all_checkbooks(current_user.id)
        # 转换成 web需要的格式
        checkbook_list = []
        for checkbook in checkbooks:
            t_check = {}
            t_check["checkbook_id"] = checkbook.id
            t_check["checkbook_name"] = checkbook.checkbook_name
            t_check["create_time"] = checkbook.create_time
            t_check["last_update_time"] = checkbook.last_update_time
            t_check["description"] = checkbook.description
            t_check["status"] = checkbook.status
            t_check["rules"] = checkbook.rules
            t_check["partner"] = []
            user_ids = json.loads(checkbook.partners)
            for user_id, permission in user_ids.items():
                t_user = UserInfo.get(id=user_id.replace("user_id-",""))
                t_check["partner"].append(t_user.user_name)
                if t_user.id == current_user.id:
                    t_check["my_permission"] = permission

            checkbook_list.append(t_check)

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
    invateMap = {}

    def __init__(self):
        self.get_parser = reqparse.RequestParser()
        self.get_parser.add_argument('checkbook_id', type=str, location='args', required=True, default=12)

        self.code_parser = reqparse.RequestParser()
        self.code_parser.add_argument('code', type=str, location='args', required=True, default=12)

    def get(self):
        args = self.get_parser.parse_args()
        checkbook_id = args.get('checkbook_id')
        # TODO 检查权限

        # 生成邀请码
        invationCode=id_generator(size=16)
        while invationCode in CheckbookInvitationCodeAPI.invateMap:
            invationCode = id_generator(size=16)
        CheckbookInvitationCodeAPI.invateMap[invationCode]={
            "checkbook_id":checkbook_id,
            "creator":current_user.id
        };
        # 返回
        print(CheckbookInvitationCodeAPI.invateMap)
        return jsonify({"invationCode":invationCode})


    def post(self):
        # 使用邀请码加入记账组
        try:
            #获得邀请码
            args = self.code_parser.parse_args()
            code = args.get('code')
            checkbook_id = CheckbookInvitationCodeAPI.invateMap.get(code)["checkbook_id"]
            user_id = current_user.id
            # TODO 检查权限、是否过期

            # 加入到数据库中
            checkbooks = Checkbook.get(id=checkbook_id)
            old_parter = json.loads(checkbooks.partners)
            old_parter["user_id-"+str(user_id)]="all" # TODO 替换成相关权限
            checkbooks.partners = json.dumps(old_parter)
            checkbooks.save()

            # 返回
            print(old_parter)
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
    decorators = [login_required]

    def __init__(self):
        self.delete_parser = reqparse.RequestParser()
        self.delete_parser.add_argument('checkbook_id', type=str, location='args', required=True)

    def get(self):
        return jsonify({})

    def put(self):
        pass

    def post(self):
        #  解析参数
        get_parser = reqparse.RequestParser()
        get_parser.add_argument('name', type=str,  required=False)
        get_parser.add_argument('description', type=str,  required=False)
        get_parser.add_argument('owner', type=str,  required=False)
        args = get_parser.parse_args()

        # 创建记账本，保存数据库
        checkbook = Checkbook()
        checkbook.checkbook_name = args["name"]
        checkbook.create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        checkbook.last_update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        checkbook.description = args["description"]
        checkbook.status = "正常"
        checkbook.partners = {}
        checkbook.partners["user_id-" + str(current_user.id)] = "all"
        checkbook.partners = json.dumps(checkbook.partners)
        checkbook.creator = current_user.id
        checkbook.save()

        # 返回成功
        return jsonify({})

    def delete(self):
        args = self.delete_parser.parse_args()
        checkbook_id = args["checkbook_id"]
        checkbook = Checkbook.get(id=checkbook_id)
        # 检查权限，只有创建者可是删除
        if checkbook.creator.id == current_user.id:
            checkbook.delete()
            return jsonify({})
        raise Exception("无权删除记账本")


class DetailsListAPI(Resource):
    """
    按照记账本，月份，获得所有明细
    """

    def __init__(self):
        self.get_parser = reqparse.RequestParser()
        self.get_parser.add_argument('checkbook_id', type=str, location='args', required=True)
        self.get_parser.add_argument('month_str', type=str, location='args', required=True)
        self.get_parser.add_argument('category', type=str, location='args', required=False, default=None)
        self.get_parser.add_argument('type', type=str, location='args', required=False, default=None)
        self.get_parser.add_argument('account_name', type=str, location='args', required=False, default=None)
        self.get_parser.add_argument('page', type=int, location='args', required=False, default=1)
        self.get_parser.add_argument('limit', type=int, location='args', required=False, default=10)
        pass

    def get(self):
        # 获得参数
        args = self.get_parser.parse_args()
        checkbook_id = args.get('checkbook_id')
        month_str = args.get('month_str')
        account_name = args.get('account_name')
        type = args.get('type')
        category = args.get('category')
        page = args.get('page')
        limit = args.get('limit')

        # 判断构造查询语句

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

    def put(self,id):
        pass

    def post(self):
        """TODO 添加一个记账明细"""
        get_parser = reqparse.RequestParser()
        get_parser.add_argument('checkbook_id', type=str, required=True)
        get_parser.add_argument('date', type=str, required=True)
        get_parser.add_argument('type', type=str, required=True)
        get_parser.add_argument('money', type=float, required=True)
        get_parser.add_argument('isCash', type=str, required=True)
        get_parser.add_argument('updater', type=str, required=True)
        get_parser.add_argument('category', type=str, required=True)
        get_parser.add_argument('account_name', type=str, required=True)
        args = get_parser.parse_args()
        print(args)

        # 检查一下 格式是否正确

        # 构造一条记账明细

        # 把记账明细返回
        pass

    def delete(self):
        get_parser = reqparse.RequestParser()
        get_parser.add_argument('detail_id', type=str, required=True)
        args = get_parser.parse_args()
        print(args)
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


api.add_resource(CheckbookListAPI, "/api/v1/checkbooks", endpoint="checkbookList")
api.add_resource(CheckbookAPI, '/api/v1/checkbook', endpoint='checkbook')
api.add_resource(CheckbookInvitationCodeAPI, '/api/v1/CheckbookInvitationCode', endpoint='CheckbookInvitationCode')

api.add_resource(DetailsListAPI, '/api/v1/details', endpoint='details')
api.add_resource(DetailsSumAPI, '/api/v1/detailsum', endpoint='detailsum')
api.add_resource(DetailsAPI, '/api/v1/detail', endpoint='detail')

api.add_resource(TrendsAPI, '/api/v1/trends/checkbooks/<checkbook_id>', endpoint='trends')

