# coding=utf-8
from flask import Flask, render_template, request, flash
from flask import abort, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import config
import json
from app_api.user import get_user_row_by_id, add_user, get_user_row,edit_user
from models import User,Wallet
from app_api.wallet import add_wallet
app = Flask(__name__)
app.config.from_object(config)
app.config['SECRET_KEY'] = '123456'


db = SQLAlchemy(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.form['idphone']
        # 返回
        formdata = data
        user_info = get_user_row_by_id(data)
    else:
        formdata=''
        user_info=''

    return render_template('main.html', user_info=user_info, formdata=formdata)


@app.route('/main', methods=['GET', 'POST'])
def main():
    error = None

    data = request.args.get('idphone', '', type=str)
    # 返回
    formdata = data
    user_info = get_user_row(User.phone==data)
    if not user_info:
        error = u'无该用户信息！'
    else:
        pass

    return render_template('main.html', user_info=user_info, formdata=formdata,error=error)


@app.route('/login')
def login():
    return render_template('login/login.html')


@app.route('/userInfo', methods=['GET', 'POST'])

def userInfo():
    data = request.args.get('id_card', '', type=str)
    # 返回
    formdata = data

    user_info = get_user_row(User.id_card==data)

    return render_template('user/userInfo.html',user_info=user_info,formdata=formdata)


# 会员添加
@app.route('/useradd', methods=['GET', 'POST'])
def useradd():

    if request.method == 'POST':
        username = request.form['username']
        id_card = request.form['id_card']
        amount = request.form['amount']
        sex = request.form['sex']
        phone = request.form['phone']
        # createtime = request.form['createtime']
        # isvip = request.form['isvip']
        note = request.form['note']

        get_userinfo1 = get_user_row(User.id_card == id_card)
        get_userinfo2 = get_user_row(User.phone == phone)

        if get_userinfo1:
            flash('id yicunzai')
        elif get_userinfo2:
            flash('phone yicunzai')
        else:
            userdata = {
                'username': username,
                'id_card': id_card,
                'phone': phone,
                'amount': amount,
                'note': note,
                # 'sex':str(sex),
                # 'create_time':createtime
            }
            add_user(userdata)
    else:
        pass
    return render_template('links/userAdd.html')



# 会员列表
@app.route('/allUsers', methods=['GET', 'POST'])
@app.route('/allUsers/<int:page>/')
def userlist(page=1):


    data = request.args.get('idphone', '', type=str)
    # 返回
    formdata = data
    con = []
    if data:
        con.append(User.phone==data)
    try:
        pagination = User.query. \
            filter(*con).\
            order_by(User.id.desc()).\
            paginate(page, 20, False)
        db.session.commit()
        print pagination
        return render_template('user/allUsers.html', pagination=pagination,formdata=formdata)
    except Exception as e:
        print e
        db.session.rollback()
        return redirect(url_for('main'))

@app.route('/changePwd')
def changePwd():
    return render_template('user/changePwd.html')


@app.route('/message')
def message():
    return render_template('message/message.html')


@app.route('/newsadd')
def newsadd():
    return render_template('news/newsAdd.html')


@app.route('/newslist', methods=['GET', 'POST'])
@app.route('/newslist/<int:page>/')
def wallet_list(page=1):

    data = request.args.get('id_card','', type=str)
    # 返回
    formdata = data
    con = []
    if data:
        con.append(Wallet.id_card==data)
    try:
        pagination = Wallet.query. \
            filter(*con). \
            order_by(Wallet.id.desc()).\
            paginate(page, 10, False)
        db.session.commit()

        return render_template('news/walletList.html',pagination=pagination,formdata=formdata)
    except Exception as e:
        print e
        db.session.rollback()
        return redirect(url_for('main'))





@app.route('/wallte', methods=['GET', 'POST'])
def wallte():

    if request.method == 'POST':

        id_card = request.form['card']
        wallet = request.form['wallet']

        user_info = get_user_row(User.id_card == id_card)

        if not user_info:
            flash('no men','error')
            return redirect(url_for('main'))
        formdata = user_info.phone

        wallet_amount = user_info.amount - int(wallet if wallet else 0)

        if wallet_amount > 0:
            user_data = {
                'amount':wallet_amount,
            }
            edit_user(user_info.id,user_data)

            wallet_data = {
                'username': user_info.username,
                'id_card': int(user_info.id_card),
                'amount': int(wallet if wallet else 0),
                'vip': user_info.vip,
            }
            result = add_wallet(wallet_data)
            if result:
                flash('add wallet_item success!')
        else:
            flash('money not enoghy','error')
            return redirect(url_for('main'))
    else:
        user_info = ''
        formdata = ''

    return render_template('main.html', user_info=user_info,formdata=formdata)


if __name__ == '__main__':
    app.run(debug=True)
