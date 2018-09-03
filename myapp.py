# _*_ coding: utf-8 _*_
from flask import Flask, render_template, request, redirect, url_for, flash, session
from exts import db, allowed_password, allowed_username, allowed_phone
from datetime import datetime
from models import Article, User
import config
from decorations import login_confirm, not_login_confirm

app = Flask(__name__)
app.debug = True
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    articles = Article.query.order_by('-create_time').all()
    return render_template('index.html', articles=articles)


@app.route('/write/', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        content = request.form.get('content')
        today = datetime.today()
        if not session.get('username', None):
            this = Article(content=content, create_time=today)
        else:
            author = User.query.filter_by(name=session.get('username')).first()
            author_id = author.id
            this = Article(content=content, create_time=today, author_id=author_id)
        db.session.add(this)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('write.html')


@app.route('/register/', methods=['GET', 'POST'])
@not_login_confirm
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        sex = request.form.get('sex')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if User.query.filter_by(name=username).first():
            flash('用户名已存在，请更换用户名重试')
            return redirect(url_for('register'))
        elif password1 != password2:
            flash('两次输入密码不一致')
            return redirect(url_for('register'))
        elif not allowed_password(password1):
            flash('密码不允许，请更换密码注册')
            return redirect(url_for('register'))
        else:
            this = User(name=username, sex=sex, password=password1)
            db.session.add(this)
            db.session.commit()
            flash('注册成功！')
            session['username'] = username
            return redirect(url_for('index'))
    else:
        return render_template('register.html')


@app.route('/login/', methods=['GET', 'POST'])
@not_login_confirm
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        this = User.query.filter_by(name=username).first()
        if this and this.password == password:
            flash('登录成功！')
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('用户名或密码错误，请重新登录')
            return redirect(url_for('login'))
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('已成功注销，请重新登录或返回首页')
    return redirect(url_for('login'))


@app.route('/my_messages/')
@login_confirm
def my_messages():
    current_user = User.query.filter_by(name=session.get('username')).first()
    articles = current_user.articles
    return render_template('my_messages.html', articles=articles)


@app.route('/today_messages/')
def today_messages():
    today = str(datetime.now().date())
    articles = Article.query.filter(Article.create_time.startswith(today)).all()
    return render_template('today_messages.html', articles=articles)


@app.route('/user/')
@login_confirm
def userpage():
    name = session.get('username')
    user = User.query.filter_by(name=name).first()
    return render_template('user.html', user=user)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
