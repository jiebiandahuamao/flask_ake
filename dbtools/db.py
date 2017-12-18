#!/usr/bin/env python
# encoding: utf-8
from flask import Flask
from sqlalchemy.inspection import inspect
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)


def get_row_by_id(model_name, pk_id):
    """
    通过 id 获取信息
    :param model_name:
    :param pk_id:
    :return: None/object
    """
    try:
        row = db.session.query(model_name).get(pk_id)
        db.session.commit()
        return row
    except Exception as e:
        db.session.rollback()
        raise e

def get_row(model_name, *args, **kwargs):
    """
    获取信息
    Usage:
        # 方式一
        get_row(User, User.id > 1)
        # 方式二
        test_condition = {
            'name': "Larry"
        }
        get_row(User, **test_condition)
    :param model_name:
    :param args:
    :param kwargs:
    :return: None/object
    """
    try:
        row = db.session.query(model_name).filter(*args).filter_by(**kwargs).first()
        db.session.commit()
        return row
    except Exception as e:
        db.session.rollback()
        raise e


def add(model_name, data):
    """
    添加信息
    :param model_name:
    :param data:
    :return: None/Value of model_obj.PK
    """
    model_obj = model_name(**data)
    try:
        db.session.add(model_obj)
        db.session.commit()
        return inspect(model_obj).identity[0]
    except Exception as e:
        db.session.rollback()
        raise e


def edit(model_name, pk_id, data):
    """
    修改信息
    :param model_name:
    :param pk_id:
    :param data:
    :return: Number of affected rows (Example: 0/1)
    """
    model_pk = inspect(model_name).primary_key[0]
    try:
        model_obj = db.session.query(model_name).filter(model_pk == pk_id)
        result = model_obj.update(data)
        db.session.commit()
        return result
    except Exception as e:
        db.session.rollback()
        raise e

def delete(model_name, pk_id):
    """
    删除信息
    :param model_name:
    :param pk_id:
    :return: Number of affected rows (Example: 0/1)
    """
    model_pk = inspect(model_name).primary_key[0]
    try:
        model_obj = db.session.query(model_name).filter(model_pk == pk_id)
        result = model_obj.delete()
        db.session.commit()
        return result
    except Exception as e:
        db.session.rollback()
        raise e