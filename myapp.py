# _*_ coding: utf-8 _*_
from flask import Flask
import config
from views import *

app = Flask(__name__)
app.debug = True
app.config.from_object(config)
db.init_app(app)

app.add_url_rule('/', view_func=Index.as_view('index'))  # 主页
app.add_url_rule('/login/', view_func=Login.as_view('login'))  # 登录
app.add_url_rule('/reg/', view_func=Register.as_view('register'))  # 注册
app.add_url_rule('/logout/', view_func=Logout.as_view('logout'))  # 注销
app.add_url_rule('/write/', view_func=Write.as_view('write'))  # 发留言
app.add_url_rule('/my_messages/', view_func=MyMessage.as_view('my_messages'))  # 我的留言
app.add_url_rule('/new/', view_func=TodayMessage.as_view('today_messages'))  # 今日最新
app.add_url_rule('/user/', view_func=UserPage.as_view('user_page'))  # 个人主页

if __name__ == '__main__':
    app.run(host='0.0.0.0')
