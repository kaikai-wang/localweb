# _*_ coding: utf-8 _*_
from flask_sqlalchemy import SQLAlchemy
import re
from flask import flash

db = SQLAlchemy()


def allowed_password(pwd):
    if not 6 <= len(pwd) <= 20:
        flash('密码长度不合法，应在6-20个字符之间')
        return False
    pattern = re.compile('[a-zA-Z0-9_]+')
    match = re.match(pattern, pwd)
    if match and len(match.group()) == len(pwd):
        return True
    else:
        flash('密码包含非法字符')
        return False


def allowed_username(username):
    if len(username) <= 15:
        return True
    else:
        return False


def allowed_phone(phone_number):
    if len(phone_number) == 11:
        pattern = re.compile('1(3\d|4[1-8]|5\d|66|7[1-4]|8\d|9[89])\d{8}')
        match = pattern.match(phone_number)
        if match:
            return True
    return False
