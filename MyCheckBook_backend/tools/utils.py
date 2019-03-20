#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/3/11 16:19 
# @Author : wangchong 
# @Email: chongwangcc@gmail.com
# @File : utils.py 
# @Software: PyCharm
import string
import random


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def get_now_str():
    """
    获得当前时间字符串，精确到秒
    :return:
    """
    from datetime import datetime
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return now_str


def account_split(account_full_name):
    """
    拆分账户
    :param account_full_name:
    :return:
    """
    account_1 = account_full_name
    account_2 = ""
    try:
        account_1, account_2 = account_full_name.split("-")
    except:
        pass
    return account_1,account_2


class AssetsSumUtils:
    """
    计算Assets 汇总信息的类
    """
    assets_fluidity_enum = ["流动资产", "固定资产", "投资资产"]
    liability_fluidity_enum = ["流动负债", "长期负债", "投资负债"]

    def __init__(self, account_enums=[]):
        self.all_result = {}
        self.sumName = "合并账户"
        self.account_enums = account_enums
        self.account_list_level1 = [self.sumName]
        for a in self.account_enums:
            if "-" not in str(a):
                self.account_list_level1.append(a)

        # 创建整个字典结构，只是没有数据而已
        for a in self.account_list_level1:
            self.all_result[a] = {}
            self.all_result[a]["总资产"] = {"data":[], "org_sum":0, "now_sum":0}
            self.all_result[a]["总负债"] = {"data":[], "org_sum":0, "now_sum":0}
            for assets in self.assets_fluidity_enum:
                self.all_result[a]["总资产"]["data"].append({
                    "name": assets,
                    "org_sum": 0,
                    "now_sum": 0,
                    "data": []
                });
            for liability in self.liability_fluidity_enum:
                self.all_result[a]["总负债"]["data"].append({
                    "name": liability,
                    "org_sum": 0,
                    "now_sum": 0,
                    "data": []
                });

    def __add_one(self, org_price,
                  now_price,
                  appendix_name,
                  account1,
                  fluidity,
                  sum_type="总资产"):
        org_price = float(org_price)
        now_price = float(now_price)
        self.all_result[account1][sum_type]["org_sum"] += org_price
        self.all_result[account1][sum_type]["now_sum"] += now_price
        self.all_result[account1][sum_type]["org_sum"] = round(self.all_result[account1][sum_type]["org_sum"], 2)
        self.all_result[account1][sum_type]["now_sum"] = round(self.all_result[account1][sum_type]["now_sum"], 2)
        for t_dict in self.all_result[account1][sum_type]["data"]:
            if t_dict["name"] == fluidity:
                t_dict["org_sum"] += org_price
                t_dict["now_sum"] += now_price
                t_dict["org_sum"] = round( t_dict["org_sum"], 2)
                t_dict["now_sum"] = round(t_dict["now_sum"], 2)
                t_apendix_dict = None
                for tt in t_dict["data"]:
                    if tt["name"] == appendix_name:
                        t_apendix_dict = tt
                if t_apendix_dict is None:
                    t_dict["data"].append({"name": appendix_name, "org_sum": org_price, "now_sum": now_price})
                    pass
                else:
                    t_apendix_dict["org_sum"] += org_price
                    t_apendix_dict["now_sum"] += now_price
                    t_apendix_dict["org_sum"] = round(t_apendix_dict["org_sum"], 2)
                    t_apendix_dict["now_sum"] = round(t_apendix_dict["now_sum"], 2)
                break

    def add(self, org_price, now_price, appendix_name, account_name, fluidity ):
        """
        添加一条记录
        :param org_price:
        :param now_price:
        :param appendix_name:
        :param fluidity:
        :param account_name:
        :return:
        """
        if account_name is None or len(account_name) == 0:
            account_name = "default"
        account1, account2 = account_split(account_name)
        if account1 not in self.account_enums:
            print(account1+ "  非法的账户名")
            return False
        if fluidity in self.assets_fluidity_enum:
            # 资产项目
            self.__add_one(org_price, now_price, appendix_name, account1, fluidity, "总资产")
            self.__add_one(org_price, now_price, appendix_name, self.sumName, fluidity, "总资产")
            pass
        elif fluidity in self.liability_fluidity_enum:
            # 负债项目
            self.__add_one(org_price, now_price, appendix_name, account1, fluidity, "总负债")
            self.__add_one(org_price, now_price, appendix_name, self.sumName, fluidity, "总负债")
            pass
        else:
            print(fluidity + " error flowtype ")
            return False

        return True


    def get_final_result(self):
        return self.all_result


if __name__ == "__main__":
    assets = AssetsSumUtils(["花销账户", "投资账户", "储蓄账户"])


