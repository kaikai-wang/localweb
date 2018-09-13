#!usr/bin/python3
# _*_ coding: utf-8 _*_
from flask.views import View, MethodView
from models import *
from flask import render_template, request, flash, session, redirect, url_for, abort
from decorations import not_login_confirm, login_confirm
from exts import allowed_password, allowed_username
from datetime import datetime
import hashlib


class Index(View):
    def dispatch_request(self):
        articles = Article.query.order_by('-create_time').all()
        return render_template('index.html', articles=articles)


class Login(MethodView):
    @not_login_confirm
    def get(self):
        return render_template('login.html')

    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')
        secret_password = hashlib.md5()
        secret_password.update(password.encode(encoding='utf-8'))
        secret_password = secret_password.hexdigest()
        this = User.query.filter_by(name=username).first()
        if this and this.password == secret_password:
            session['username'] = username
            if username == 'admin':
                return redirect(url_for('admin.admin_index'))
            else:
                flash('登录成功！')
                return redirect(url_for('index'))
        flash('用户名或密码错误，请重新登录')
        return redirect(url_for('login'))


class Register(MethodView):
    @not_login_confirm
    def get(self):
        return render_template('register.html')

    def post(self):
        username = request.form.get('username')
        sex = request.form.get('sex')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if not allowed_username(username):
            flash('用户名长度过长，请更换用户名')
            return redirect(url_for('register'))
        elif User.query.filter_by(name=username).first():
            flash('用户名已存在，请更换用户名')
            return redirect(url_for('register'))
        elif password1 != password2:
            flash('两次输入密码不一致')
            return redirect(url_for('register'))
        elif not allowed_password(password1):
            flash('密码不允许，请更换密码注册')
            return redirect(url_for('register'))
        else:
            secret_password = hashlib.md5()
            secret_password.update(password1.encode(encoding='utf-8'))
            secret_password = secret_password.hexdigest()
            assert len(secret_password) < 50, 'password length error'
            this = User(name=username, sex=sex, password=secret_password)
            db.session.add(this)
            db.session.commit()
            flash('注册成功')
            session['username'] = username
            return redirect(url_for('index'))


class Logout(View):
    def dispatch_request(self):
        session.clear()
        flash('已退出，请重新登录')
        return redirect(url_for('index'))


class Write(MethodView):
    def get(self):
        return render_template('write.html')

    def post(self):
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
        flash('留言成功')
        return redirect(url_for('index'))


class MyMessage(View):
    def dispatch_request(self):
        current_user = User.query.filter_by(name=session.get('username')).first()
        articles = current_user.articles
        return render_template('my-messages.html', articles=articles)


class TodayMessage(View):
    def dispatch_request(self):
        today = str(datetime.now().date())
        articles = Article.query.filter(Article.create_time.startswith(today)).all()
        return render_template('today_messages.html', articles=articles)


class UserPage(View):
    @login_confirm
    def dispatch_request(self):
        this = User.query.filter_by(name=session.get('username')).first()
        return render_template('user.html', user=this)


class OtherUser(View):
    def dispatch_request(self, id=None):
        this = User.query.filter_by(id=id).first()
        if not this:
            abort(404)
        elif this.name == session.get('username'):
            return redirect(url_for('user_page'))
        else:
            return render_template('other-user.html', user=this)


class Detail(View):
    def dispatch_request(self, id=None):
        this = Article.query.filter_by(id=id).first()
        if not this:
            return abort(404)
        return render_template('detail.html', article=this)


class UserMessages(View):
    def dispatch_request(self, id=None):
        this_user = User.query.filter_by(id=id).first()
        articles = this_user.articles
        return render_template('user-messages.html', articles=articles)


class ChangeSex(MethodView):
    @login_confirm
    def get(self):
        username = session.get('username')
        this_user = User.query.filter_by(name=username).first()
        return render_template('change-sex.html', user=this_user)

    def post(self):
        sex = request.form.get('sex')
        username = session.get('username')
        this_user = User.query.filter_by(name=username).first()
        this_user.sex = sex
        db.session.commit()
        return redirect(url_for('user_page'))


class ChangePwd(MethodView):
    @login_confirm
    def get(self):
        return render_template('change-pwd.html')

    def post(self):
        username = session.get('username')
        old_password = request.form.get('old_password')
        print(old_password)
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if not username:
            abort(404)
        else:
            this_user = User.query.filter_by(name=username).first()
            op = hashlib.md5()
            op.update(old_password.encode(encoding='utf8'))
            print(op.hexdigest(), this_user.password)
            if this_user.password != op.hexdigest():
                flash('输入用户密码不正确')
                return redirect(url_for('change_pwd'))
            elif password1 != password2:
                flash('两次新密码输入不一致')
                return redirect(url_for('change_pwd'))
            elif not allowed_password(password1):
                return redirect(url_for('change_pwd'))
            else:
                secret_password = hashlib.md5()
                secret_password.update(password1.encode(encoding='utf-8'))
                this_user.password = secret_password.hexdigest()
                db.session.commit()
                flash('密码修改成功')
                return redirect(url_for('user_page'))

