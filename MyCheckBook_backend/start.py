#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/3/5 11:05 
# @Author : wangchong 
# @Email: chongwangcc@gmail.com
# @File : start.py.py 
# @Software: PyCharm


from tools.app import app
from tools.web_html import *
from tools.restful_v2 import *


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=7001)