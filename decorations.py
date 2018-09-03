#!usr/bin/python3
# _*_ coding: utf-8 _*_
from functools import wraps
from flask import session, flash, redirect, url_for


def login_confirm(func):
    @wraps(func)
    def decoration(*args, **kwargs):
        if session.get('username', None):
            return func()
        else:
            flash('当前未登录，请在此页进行登录')
            return redirect(url_for('login'))
    return decoration


def not_login_confirm(func):
    @wraps(func)
    def decoration(*args, **kwargs):
        if not session.get('username', None):
            return func()
        else:
            return redirect(404)
    return decoration
