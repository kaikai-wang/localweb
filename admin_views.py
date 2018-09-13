# _*_ coding: utf-8 _*_
from flask import Blueprint, render_template, redirect, url_for
from models import Article, User
from exts import db
from decorations import is_admin

admin = Blueprint('admin', __name__)


# 留言管理
@admin.route('/')
@is_admin
def admin_index():
    articles = Article.query.order_by('-create_time').all()
    for article in articles:
        print(article.content)
    return render_template('admin-index.html', articles=articles)


# 留言删除
@admin.route('/del/<int:id>')
@is_admin
def admin_delete(id):
    this = Article.query.filter_by(id=id).first()
    db.session.delete(this)
    db.session.commit()
    return redirect(url_for('admin.admin_index'))


# 留言详情页
@admin.route('/detail/<int:id>')
@is_admin
def admin_detail(id):
    this = Article.query.filter_by(id=id).first()
    return render_template('admin-detail.html', article=this)


# 用户管理
@admin.route('/users/')
@is_admin
def admin_users():
    all_user = User.query.all()
    return render_template('admin-users.html', users=all_user)


# 删除用户
@admin.route('/del_user/<int:id>')
@is_admin
def admin_del_user(id):
    this_user = User.query.filter_by(id=id).first()
    if this_user:
        db.session.delete(this_user)
        db.session.commit()
    return redirect(url_for('admin.admin_users'))


