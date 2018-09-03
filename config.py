# _*_ coding: utf-8 _*_
# dialect+driver://username:password@host:port/database
from os import urandom

dialect = 'mysql'
driver = 'mysqldb'
username = 'root'
password = 'root'
db_host = '127.0.0.1'
port = '3307'
database = 'flaskdb'

SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}'.format(dialect, driver, username, password,
                                                          db_host, port, database)
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = 'sao3ksk4z4d9ca5'
