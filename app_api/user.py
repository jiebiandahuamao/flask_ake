#!/usr/bin/env python
# encoding: utf-8

from dbtools.db import get_row_by_id, get_row, add, edit, delete, get_list
from models import User


def get_user_row_by_id(user_id):
    """
    通过 id 获取用户信息
    :param user_id:
    :return: None/object
    """
    return get_row_by_id(User, user_id)

def get_user_row(*args, **kwargs):
    """
    获取用户信息
    :param args:
    :param kwargs:
    :return: None/object
    """
    return get_row(User, *args, **kwargs)

def get_user_list(*args, **kwargs):
    """
    获取user信息list
    :param args:
    :param kwargs:
    :return: None/object
    """
    return get_list(User, *args, **kwargs)


def add_user(user_data):
    """
    添加用户信息
    :param user_data:
    :return: None/Value of user.id
    """
    return add(User, user_data)

def edit_user(user_id, user_data):
    """
    修改用户信息
    :param user_id:
    :param user_data:
    :return: Number of affected rows (Example: 0/1)
    """
    return edit(User, user_id, user_data)

def delete_user(user_id):
    """
    删除用户信息
    :param user_id:
    :return: Number of affected rows (Example: 0/1)
    """
    return delete(User, user_id)
