# coding=utf-8
from flask import Flask, render_template, request, flash
from flask import abort, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import config
from app_api.user import get_user_row_by_id, add_user, get_user_row, edit_user, get_user_list
from models import User, Wallet, Admin
from app_api.wallet import add_wallet, get_wallet_list
from dbtools.time import get_today_time
from flask_login import LoginManager, login_user, login_required, logout_user

app = Flask(__name__)
app.config.from_object(config)
app.config['SECRET_KEY'] = u'123456'

login_manager = LoginManager()
login_manager.init_app(app)

db = SQLAlchemy(app)

login_manager.login_view = u"login"  # 定义登录的 视图
login_manager.login_message = u'请登录以访问此页面'  # 定义需要登录访问页面的提示消息

@login_manager.user_loader  # 使用user_loader装饰器的回调函数非常重要，他将决定 user 对象是否在登录状态
def user_loader(id):  # 这个id参数的值是在 login_user(user)中传入的 user 的 id 属性

    user = Admin.query.filter_by(id=id).first()
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        name = request.form['username']
        user = Admin.query.filter_by(username=name).first()
        if not user:
            pass
            # flash(u'该用户不存在')
        elif request.form['password'] != user.password:
            pass
            # flash(u'密码错误')
        else:
            login_user(user)
            next_url = request.args.get('next')
            flash(u'欢迎登录ake!')
            return redirect(next_url or url_for('main'))

    return render_template('login/login.html')

@app.route('/logout/')
@login_required
def logout():
    logout_user()  # 登出用户
    return u'已经退出登录'

@app.route('/', methods=['GET', 'POST'])
@login_required
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
@login_required
def main():
    error = None

    data = request.args.get('idphone', '', type=str)
    # 返回
    formdata = data
    if len(data)==11:
        user_info = get_user_row(User.phone==data)
    else:
        user_info = get_user_row(User.id_card == data)
    if not user_info:
        error = u'无该用户信息！'
    else:
        pass

    return render_template('main.html', user_info=user_info, formdata=formdata,error=error)

#修改用户信息
@app.route('/userInfo', methods=['GET', 'POST'])
@login_required
def userInfo():

    data = request.args.get('user_id', '', type=str)
    user_info = get_user_row_by_id(data)

    if request.method == 'POST':
        user_id = request.form['user_id']
        username = request.form['username']
        id_card = request.form['id_card']
        amount = request.form['amount']
        phone = request.form['phone']
        isvip = request.form['isvip']
        note = request.form['note']
        user_pro = get_user_row_by_id(user_id)
        flag = True

        if user_pro.id_card != long(id_card):
            if get_user_row(User.id_card == long(id_card)):
                flag = False
                flash(u'卡号 已存在 不能重复!')

        if user_pro.phone != phone:
            if get_user_row(User.phone == phone):
                flag = False
                flash(u'该电话号码已存在,请确认!')

        if isvip =='on':
            vip=1
        else:
            vip=0

        if flag == True:
            userdata = {
                'username': username,
                'id_card': id_card,
                'phone': phone,
                'amount': amount,
                'note': note,
                'vip':vip,
            }
            edit_user(user_id, userdata)
            flash(u'修改用户信息成功')
        else:
            flash(u'修改用户信息失败')
        user_info = get_user_row_by_id(user_id)
    else:
        pass
    return render_template('user/userInfo.html', user_info=user_info)

# 会员添加
@app.route('/useradd', methods=['GET', 'POST'])
@login_required
def useradd():

    if request.method == 'POST':
        username = request.form['username']
        id_card = request.form['id_card']
        amount = request.form['amount']
        phone = request.form['phone']
        isvip = request.form['isvip']
        note = request.form['note']

        get_userinfo1 = get_user_row(User.id_card == id_card)
        get_userinfo2 = get_user_row(User.phone == phone)

        if isvip == 'on':
            vip = 1
        else:
            vip = 0

        if get_userinfo1:
            flash(u'卡号 已存在 不能重复!')
        elif get_userinfo2:
            flash(u'该电话号码已存在,请确认!')
        else:
            userdata = {
                'username': username,
                'id_card': id_card,
                'phone': phone,
                'amount': amount,
                'note': note,
                'vip':vip,
            }
            add_user(userdata)
            flash(u'添加用户成功!')
    else:
        pass
    return render_template('links/userAdd.html')

#会员删除
@app.route('/userdel', methods=['GET', 'POST'])
@login_required
def userdel():

    data = request.args.get('user_id', '', type=str)
    user_info = get_user_row_by_id(data)
    if user_info:
        user_data = {
            'dele': 1
        }
        edit_user(data,user_data)
        flash(u"删除用户成功!")
    else:
        flash(u'无此用户信息')

    return redirect(url_for('userlist'))

# 会员列表
@app.route('/allUsers', methods=['GET', 'POST'])
@app.route('/allUsers/<int:page>/')
@login_required
def userlist(page=1):

    data = request.args.get('idphone', '', type=str)
    # 返回
    formdata = data
    con = [User.dele == 0]
    if data:
        con.append(User.phone==data or User.id_card==data)
    try:
        pagination = User.query. \
            filter(*con).\
            order_by(User.id.desc()).\
            paginate(page, 25, False)
        db.session.commit()

        return render_template('user/allUsers.html', pagination=pagination,formdata=formdata)
    except Exception as e:
        print e
        db.session.rollback()
        return redirect(url_for('main'))

@app.route('/changePwd')
@login_required
def changePwd():
    return render_template('user/changePwd.html')

#统计数据
@app.route('/countdata')
@login_required
def count_data():

    start_time,end_time = get_today_time()

    #今日消费金额
    con = [start_time<=Wallet.create_time,
           end_time >= Wallet.create_time,
           Wallet.wallet_type == 0
        ]
    get_wallet_todayrows = get_wallet_list(*con)

    wallet_today = {
        'money':sum(i.amount for i in get_wallet_todayrows),
        'count':len(get_wallet_todayrows)
    }

    # 今日充值金额
    cons = [start_time <= Wallet.create_time,
           end_time >= Wallet.create_time,
           Wallet.wallet_type == 1
           ]
    get_addwallet_todayrows = get_wallet_list(*cons)

    addwallet_today = {
        'money':sum(i.amount for i in get_addwallet_todayrows),
        'count':len(get_addwallet_todayrows)
    }

    #消费金额
    get_wallet_rows = get_wallet_list(Wallet.wallet_type==0)
    wallte_his = {
        'money':sum(i.amount for i in get_wallet_rows),
        'count':len(get_wallet_rows)
    }

    #充值金额
    get_add_rows = get_wallet_list(Wallet.wallet_type == 1)
    addwallte_his = {
        'money':sum(i.amount for i in get_add_rows),
        'count':len(get_add_rows)
    }

    #获取user
    get_user_count = len(get_user_list())
    get_vipuser_count = len(get_user_list(User.vip==1))

    return render_template('count_data/count_data.html',wallet_today=wallet_today,addwallet_today=addwallet_today,
                           wallte_his=wallte_his,addwallte_his=addwallte_his,get_user_count=get_user_count,
                           get_vipuser_count=get_vipuser_count)

@app.route('/newsadd')
@login_required
def newsadd():
    return render_template('news/newsAdd.html')


@app.route('/newslist', methods=['GET', 'POST'])
@app.route('/newslist/<int:page>/')
@login_required
def wallet_list(page=1):

    data = request.args.get('id_card','', type=str)
    type = request.args.get('type', '', type=str)
    # 返回
    formdata = data
    con = []
    if data:
        con.append(Wallet.id_card==data)
    if type:
        con.append(Wallet.wallet_type==type)
    try:
        pagination = Wallet.query. \
            filter(*con). \
            order_by(Wallet.id.desc()).\
            paginate(page, 20, False)
        db.session.commit()

        return render_template('news/walletList.html',pagination=pagination,formdata=formdata)
    except Exception as e:
        print e
        db.session.rollback()
        return redirect(url_for('main'))

@app.route('/wallte', methods=['GET', 'POST'])
@login_required
def wallte():

    if request.method == 'POST':

        id_card = request.form['card']
        wallet = request.form['wallet']

        user_info = get_user_row(User.id_card == id_card)

        if not user_info:
            flash(u'无此用户信息')
            return redirect(url_for('main'))
        formdata = user_info.phone

        wallet_amount = float(user_info.amount) - float(wallet if wallet else 0)

        if wallet_amount >= 0:
            user_data = {
                'amount':wallet_amount,
            }
            edit_user(user_info.id,user_data)

            wallet_data = {
                'username': user_info.username,
                'id_card': int(user_info.id_card),
                'amount': float(wallet if wallet else 0),
                'vip': user_info.vip,
            }
            result = add_wallet(wallet_data)
            if result:
                flash(u'用户%s消费%s元' % (user_info.username,wallet))
        else:
            flash(u'用户剩余金额不够了!')
    else:
        user_info = ''
        formdata = ''

    return render_template('main.html', user_info=user_info,formdata=formdata)

#会员充值
@app.route('/add_wallte', methods=['GET', 'POST'])
@login_required
def add_wallte():

    if request.method == 'POST':

        add_data = request.form['add_money']
        user_id = request.form['user_id']

        user_info = get_user_row_by_id(user_id)
        formdata = user_info.id_card if user_info else ''

        if user_info:
            user_data = {
                'amount':float(user_info.amount) + float(add_data)
            }
            edit_user(user_id, user_data)

            wallet_data = {
                'username': user_info.username,
                'id_card': int(user_info.id_card),
                'amount': float(add_data),
                'vip': user_info.vip,
                'wallet_type':1,    #0消费,1充值
            }
            result = add_wallet(wallet_data)
            if result:
                flash(u'会员%s成功充值%s元' % (user_info.username,add_data))
            else:
                flash(u'充值失败!')
        else:
            flash(u'无此用户信息')
    else:
        user_info = ''
        formdata = ''

    return render_template('main.html', user_info=user_info,formdata=formdata)

if __name__ == '__main__':
    app.run(debug=True)
