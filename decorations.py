#!usr/bin/python3
# _*_ coding: utf-8 _*_
from functools import wraps
from flask import session, flash, redirect, url_for, abort


def login_confirm(func):
    @wraps(func)
    def decoration(*args, **kwargs):
        if session.get('username', None):
            return func(*args, **kwargs)
        else:
            flash('当前未登录，请在此页进行登录')
            return redirect(url_for('login'))
    return decoration


def not_login_confirm(func):
    @wraps(func)
    def decoration(*args, **kwargs):
        if not session.get('username', None):
            return func(*args, **kwargs)
        else:
            abort(404)
    return decoration


def is_admin(func):
    @wraps(func)
    def decoration(*args, **kwargs):
        if session.get('username', None) == 'admin':
            return func(*args, **kwargs)
        else:
            flash('没有访问权限')
            return redirect(url_for('index'))
    return decoration

