from flask_sqlalchemy import SQLAlchemy
import yagmail
import redis

db = SQLAlchemy()
yag_server = yagmail.SMTP(user='******', password='******', host='smtp.qq.com')
conn_pool = redis.ConnectionPool(host='localhost',port=6379)