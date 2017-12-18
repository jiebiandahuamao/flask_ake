#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: __init__.py.py
@time: 2017/4/19 下午2:24
"""

from logging.config import dictConfig

from flask import Flask



app = Flask(__name__)
app.config.from_object('config')