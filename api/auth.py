# coding:utf-8
from api import api_bp
from flask import request,abort,current_app,jsonify
from datetime import datetime, timedelta
from .models import db,User,token_required
import json
import redis
import re
import uuid
import yagmail

yag_server = yagmail.SMTP(user='******', password='******', host='smtp.qq.com')


def expire(name, exp=60):
    """
    设置过期时间
    """
    r = redis.StrictRedis('127.0.0.1', '6379', 1)
    r.expire(name, exp)

def hset(name, key, value):
    """
    设置指定hash表
    :return:
    """
    r = redis.StrictRedis('127.0.0.1', '6379', 1)
    r.hset(name, key, value)

def hget(name, key):
    """
    读取指定hash表的键值
    """
    r = redis.StrictRedis('127.0.0.1', '6379', 1)
    value = r.hget(name, key)
    print(value)
    return value.decode('utf-8') if value else value

def check_mail(mail):
    """
    验证前端传入的是否为邮箱
    :param mail:邮箱
    :return:
    """
    _mail = re.match(r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$', mail)
    if _mail is None:
        return None
    else:
        return _mail.group()

def check_mail_code(mail, code):
    """
    验证邮箱和验证码是否正确
    :param mail: 邮箱
    :param code: 验证码
    :return:
    """
    mail = check_mail(mail)
    if mail is None:
        return False
    else:
        _code = hget(mail, "code")
        print(_code)
        if code == _code:
            return True
        else:
            return False

def login_or_register(_mail):
    user_login = User.query.filter_by(mail = _mail).first()
    if user_login: #用户存在则直接返回
        user = User.query.filter_by(id=user_login.id).first()
        return user
    else:
        try:
            new_user = User(name="nickname", mail=_mail, user_group=0, token=None)
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            print(e)
            return None
        return new_user

#apis below

@api_bp.route('/email_captcha', methods=['GET', 'POST'])
def email_captcha():
    """
    获取邮箱验证码
    """
    now = datetime.now()
    mail = request.get_json(force=True).get('mail',None)
    mail = check_mail(mail)
    if mail is None:
        return jsonify({"status":"failure","message":"invalid email address"})
    last_time = hget(mail, 'expire_time')
    if last_time is not None:
        last_time = datetime.strptime(last_time, '%Y-%m-%d %H:%M:%S')
        if (last_time - now).total_seconds() < 60:
            return jsonify({"status":"failure","message":"requests are too frequent"})
    #随机验证码
    code = str(uuid.uuid1())[:6]
    #try:
    print(yag_server.send([mail],"aaa",'bbb:%s' % code))
    hset(mail, "code", code)  #验证码存入redis
    hset(mail, "expire_time", (now + timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M:%S'))
    expire(mail, 60 * 10)  #设置过期时间
    return jsonify({"status":"success","message":"ok"})
    #except Exception as e:
        #print(e)
        #return abort(500)
    
@api_bp.route('/login', methods=['GET', 'POST'])
def login():
    request_data = request.get_json(force=True)
    mail = request_data.get('mail', None)
    code = request_data.get('code', None)
    if mail is None or code is None:
        return jsonify({"status":"failure","message":"get empty param"})
    flag = check_mail_code(mail, code)
    if not flag:
        return jsonify({"status":"failure","message":"wrong code"})
    user = login_or_register(mail)
    if user is None:
        return jsonify({"status":"failure","message":"unable to create"})
    return jsonify({"status":"success","message":"ok","token":user.generate_auth_token(expiration=60*60)})

@api_bp.route('/test_token', methods=['GET', 'POST'])
@token_required
def test_token():
    return 'okok'