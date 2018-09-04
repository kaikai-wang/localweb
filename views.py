#!usr/bin/python3
# _*_ coding: utf-8 _*_
from flask.views import View, MethodView
from models import *
from flask import render_template, request, flash, session, redirect, url_for
from decorations import not_login_confirm, login_confirm
from exts import allowed_password, allowed_username
from datetime import datetime


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
        this = User.query.filter_by(name=username).first()
        if this and this.password == password:
            flash('登录成功！')
            session['username'] = username
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
            this = User(name=username, sex=sex, password=password1)
            db.session.add(this)
            db.session.commit()
            flash('注册成功！')
            session['username'] = username
            return redirect(url_for('index'))


class Logout(View):
    def dispatch_request(self):
        session.clear()
        flash('已成功注销，请重新登录')
        return redirect(url_for('login'))


class Write(MethodView):
    @login_confirm
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
        return render_template('my_messages.html', articles=articles)


class TodayMessage(View):
    def dispatch_request(self):
        today = str(datetime.now().date())
        articles = Article.query.filter(Article.create_time.startswith(today)).all()
        return render_template('today_messages.html', articles=articles)


class UserPage(View):
    def dispatch_request(self):
        name = session.get('username')
        user = User.query.filter_by(name=name).first()
        return render_template('user.html', user=user)