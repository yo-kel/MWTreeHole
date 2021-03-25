'''
共享使用的第三方库内容
'''
from flask_sqlalchemy import SQLAlchemy
import yagmail
import redis

db = SQLAlchemy()
yag_server = yagmail.SMTP(user='******', password='******', host='smtp.qq.com')
conn_pool = redis.ConnectionPool(host='localhost', port=6379)

# redis接口的封装
def expire(name, exp=60):
    """
    设置过期时间
    """
    r = redis.StrictRedis(connection_pool=conn_pool)
    r.expire(name, exp)

def hset(name, key, value):
    """
    设置指定hash表
    """
    r = redis.StrictRedis(connection_pool=conn_pool)
    r.hset(name, key, value)

def hget(name, key):
    """
    读取指定hash表的键值
    """
    r = redis.StrictRedis(connection_pool=conn_pool)
    value = r.hget(name, key)
    return value.decode('utf-8') if value else value