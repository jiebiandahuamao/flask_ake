#!/usr/bin/env python
# encoding: utf-8

from flask import redirect,Flask
from flask import render_template, request, flash

from app_api.user import get_user_row_by_id

app = Flask(__name__)
app.config.from_object(config)

@app.route('/',methods=['GET','POST'])
def index():

    return render_template('main.html')

@app.route('/main',methods=['GET','POST'])
def main():

    if request.method == 'POST':
        data = request.form['idphone']
        user_info = get_user_row_by_id(data)
        print user_info,"&&&&&&&&&"

    return render_template('main.html')
