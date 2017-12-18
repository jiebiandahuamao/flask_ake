#!/usr/bin/env python
# encoding: utf-8


from dbtools import get_row_by_id, get_row, add, edit, delete
from models import Admin


def get_admin_row_by_id(user_auth_id):
    """
    通过 id 获取用户信息
    :param user_auth_id:
    :return: None/object
    """
    return get_row_by_id(Admin, user_auth_id)


def get_admin_row(*args, **kwargs):
    """
    获取用户信息
    :param args:
    :param kwargs:
    :return: None/object
    """
    return get_row(Admin, *args, **kwargs)


def add_admin(user_auth_data):
    """
    添加用户信息
    :param user_auth_data:
    :return: None/Value of user.id
    """
    return add(Admin, user_auth_data)


def edit_admin(user_auth_id, user_auth_data):
    """
    修改用户信息
    :param user_auth_id:
    :param user_auth_data:
    :return: Number of affected rows (Example: 0/1)
    """
    return edit(Admin, user_auth_id, user_auth_data)


def delete_admin(user_auth_id):
    """
    删除用户信息
    :param user_auth_id:
    :return: Number of affected rows (Example: 0/1)
    """
    return delete(Admin, user_auth_id)