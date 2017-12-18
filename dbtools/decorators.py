#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: decorators.py
@time: 16-3-11 下午3:08
"""


import functools
import os
import traceback
from threading import Thread

from flask import g


def async(f):
    """
    基于线程的异步调用装饰器
    :param f:
    :return:
    """
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper


def log_request(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        g.log_info['func_name'] = f.func_name
        g.log_info['args'] = [str(a) for a in args]
        g.log_info['pid'] = os.getpid()
        if kwargs:
            g.log_info['kwargs'] = kwargs
        try:
            ret = f(*args, **kwargs)
            if hasattr(g, 'current_user_id'):
                g.log_info['user_id'] = g.current_user_id
            else:
                g.log_info['user_id'] = 0
            if hasattr(ret, 'response') and f.func_name != 'get_code':
                g.log_info['ret'] = ret.response
            else:
                g.log_info['ret'] = ''
        except:
            g.log_info['format_exc'] = traceback.format_exc()
            g.log_info['ret'] = ''
            raise
        return ret
    return decorated
