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
        mtype = args.get('type')
        category = args.get('category')
        page = args.get('page')
        limit = args.get('limit')

        # 判断构造查询语句
        detail_df = get_Details(checkbook_id, month_str, account_name, mtype, category)
        start_index = (page-1)*limit
        end_index =len(detail_df) if page*limit > len(detail_df) else page*limit;
        all_nums = len(detail_df)
        detail_df = detail_df[start_index:end_index]
        detail_df.sort_values(by=["date"], ascending=False)

        # 构造返回结果
        data = []
        checkbook_info = Checkbook.get(id=checkbook_id)
        for index,row in detail_df.iterrows():
            t_detail = {}
            t_detail["detail_id"] = row["id"]
            t_detail["date"] = row["date"]
            t_detail["money"] = row["money"]
            t_detail["category"] = row["category"]
            t_detail["remark"] = row["remark"]
            t_detail["isCash"] = row["isCash"]
            t_detail["type"] = row["type"]
            t_detail["account_name"] = row["account_name"]
            t_detail["seconds_account_name"] = row["seconds_account_name"]
            t_detail["updater"] = UserTools.gen_id_to_name(row["updater"])
            t_detail["checkbook_name"] = checkbook_info.checkbook_name
            data.append(t_detail)

        result={
            "code":0,
            "msg":"",
            "count":all_nums,
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
        pass

    def get(self):
        args = self.get_parser.parse_args()
        checkbook_id = args.get('checkbook_id')
        month_str = args.get('month_str')

        # 1. 获得明细数据
        detail_df = get_Details(checkbook_id, month_str, None, None, None)

        # 2. 聚合 获得结果
        category_sum = detail_df.groupby(['type', 'category'])["money"].sum().reset_index()
        account_sum = detail_df.groupby(['type', 'account_name','seconds_account_name'])["money"].sum().reset_index()
        # 3.构造返回结果
        result={
            "income_category":{
                "legend":[],
                "sumType": "总收入",
                "sumValue": 0,
                "data": []
            },
            "income_account": {
                "legend": [],
                "sumType": "总收入",
                "sumValue": 0,
                "data1": [],
                "data2": []
            },
            "spent_category": {
                "legend": [],
                "sumType": "总支出",
                "sumValue": 0,
                "data": []
            },
            "spent_account": {
                "legend": [],
                "sumType": "总支出",
                "sumValue": 0,
                "data1": [],
                "data2": []
            },
            "inflow_category": {
                "legend": [],
                "sumType": "总流入",
                "sumValue": 0,
                "data": []
            },
            "inflow_account": {
                "legend": [],
                "sumType": "总流入",
                "sumValue": 0,
                "data1": [],
                "data2": []
            },
            "outflow_category": {
                "legend": [],
                "sumType": "总流出",
                "sumValue": 0,
                "data": []
            },
            "outflow_account": {
                "legend": [],
                "sumType": "总流出",
                "sumValue": 0,
                "data1": [],
                "data2": []
            },

        }
        for index, row in category_sum.iterrows():
            mtype = row["type"]
            category = row["category"]
            money = row["money"]
            if mtype == "支出":
                result["spent_category"]["legend"].append(category)
                result["spent_category"]["sumValue"]+= money
                result["spent_category"]["data"].append({"value":money, "name":category})
                pass
            elif mtype == "收入":
                result["income_category"]["legend"].append(category)
                result["income_category"]["sumValue"] += money
                result["income_category"]["data"].append({"value": money, "name": category})
            elif mtype == "流入":
                result["inflow_category"]["legend"].append(category)
                result["inflow_category"]["sumValue"] += money
                result["inflow_category"]["data"].append({"value": money, "name": category})
            elif mtype == "流出":
                result["outflow_category"]["legend"].append(category)
                result["outflow_category"]["sumValue"] += money
                result["outflow_category"]["data"].append({"value": money, "name": category})

        last_type, last_account_name, last_index_name, last_money = None, None,None, 0
        for index, row in account_sum.iterrows():
            mtype = row["type"]
            account_name = row["account_name"]
            seconds_account_name = row["seconds_account_name"]
            money = row["money"]
            index_name = None;
            if mtype == "支出":
                index_name = "spent_account"
            elif mtype == "收入":
                index_name = "income_account"
            elif mtype == "流入":
                index_name = "inflow_account"
            elif mtype == "流出":
                index_name = "outflow_account"

            result[index_name]["legend"].append(account_name + "-" + seconds_account_name)
            result[index_name]["sumValue"] += money
            result[index_name]["data2"].append(
                {"value": money, "name": account_name + "-" + seconds_account_name})
            # 计算account 总和
            if (last_type is not None and (last_type != mtype or last_account_name != account_name)) \
                    or (index == len(account_sum)-1):
                result[last_index_name]["data1"].append({"value": last_money, "name": last_account_name})
                result[last_index_name]["legend"].append(last_account_name)
                last_money = money
            else:
                last_money +=money
            last_account_name = account_name
            last_type = mtype
            last_index_name = index_name

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
        # 0 .取参数
        get_parser = reqparse.RequestParser()
        get_parser.add_argument('detail_id', type=str, required=True)
        args = get_parser.parse_args()
        detail_id= int(args["detail_id"])

        # 1.删除
        # TODO 如果需要同步的化，要变成“标记删除”
        detail_info = DetailInfo.get(id=detail_id)
        detail_info.delete()

        # 2.返回值
        return jsonify({"msg":"success"})


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

