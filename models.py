#coding=utf-8
from flask import Flask
from sqlalchemy import text,DateTime,Numeric
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

Base = db.Model
metadata = Base.metadata


def to_dict(self):
    """
    model 对象转 字典
    model_obj.to_dict()
    """
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

Base.to_dict = to_dict
class Admin(Base):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(320), unique=True)
    password = db.Column(db.String(32), nullable=False)

class User(Base):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    id_card = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String(20), unique=True,nullable=False)
    password = db.Column(db.String(32))
    amount = db.Column(Numeric(10, 2), nullable=False, server_default=text("'0.00'"))
    vip = db.Column(db.Integer, nullable=True, server_default=text("'0'"))
    sex= db.Column(db.String(80),server_default=text("'0'"))
    note = db.Column(db.String(200), nullable=True)
    create_time = db.Column(DateTime, nullable=True, server_default=text("CURRENT_TIMESTAMP"))

class Wallet(Base):
    __tablename__ = 'wallet'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    id_card = db.Column(db.Integer, nullable=False)
    amount = db.Column(Numeric(10, 2), nullable=False, server_default=text("'0.00'"))
    vip = db.Column(db.Integer, nullable=True, server_default=text("'0'"))
    create_time = db.Column(DateTime, nullable=True, server_default=text("CURRENT_TIMESTAMP"))
