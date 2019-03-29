#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/2/25 5:28 
# @Author : wangchong 
# @Email: chongwangcc@gmail.com
# @File : setup.py.py 
# @Software: PyCharm

from setuptools import setup, find_packages

requires=[]
with open("requirements.txt", mode="r", encoding="utf8") as f:
    for line in f.readlines():
        requires.append(line.strip())

setup(name='mycheckbook_backend',

      version='0.1',

      url='https://github.com/chongwangcc/MyCheckBook_backstage',

      license='MIT',

      author='chongwangcc',

      author_email='chongwangcc@gmail.com',

      description='record and analysis where is you  money spent?',

      packages=find_packages(exclude=['mycheckbook_backend']),

      include_package_data=True,

      long_description=open('README.md', encoding="utf8").read(),

      zip_safe=False,

      setup_requires=requires,

       package_dir={'': 'mycheckbook_backend'}
      )