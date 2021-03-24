'''
用户认证(登录/注册)相关api
'''
import json
import re
import uuid
from datetime import datetime, timedelta

from flask import request, abort, current_app, jsonify, Response

from api import api_bp

from .extensions import db, yag_server, conn_pool
from .extensions import expire, hset, hget
from .decorator import token_required
from .models import User
from .enc import encrypt_data

@api_bp.route('/email_captcha', methods=['GET', 'POST'])
def email_captcha():
    """
    获取邮箱验证码
    """
    mail = request.get_json(force=True).get('mail', None)
    mail = check_mail(mail)
    if mail is None:
        return jsonify({"status": "failure", "message": "invalid email address"})
    # 防止同一邮箱频繁请求
    now = datetime.now()
    last_time = hget(mail, 'expire_time')
    if last_time is not None:
        last_time = datetime.strptime(last_time, '%Y-%m-%d %H:%M:%S')
        if (last_time - now).total_seconds() < 60:
            return jsonify({"status": "failure", "message": "requests are too frequent"})
    
    code = str(uuid.uuid1())[:6]
    yag_server.send([mail], "[MWTreeHole]Verification Code", 'Verification Code:%s' % code)

    hset(mail, "code", code)  #验证码存入redis
    hset(mail, "expire_time", (now + timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M:%S'))
    expire(mail, 60 * 10)  #设置验证码过期时间
    return jsonify({"status":"success","message":"ok"})
    
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
        return jsonify({"status": "failure", "message": "unable to create"})
    token = user.generate_auth_token(expiration=60 * 60 * 24) # 签发一天有效期的token
    outdate=datetime.today() + timedelta(days=1)
    response = Response(json.dumps({"status": "success", "message": "ok", "token": str(token)}), content_type='application/json')
    response.set_cookie("token", token, expires=outdate)
    return response

def check_mail(mail):
    """
    验证前端传入的是否为邮箱
    :param mail:邮箱
    :return:邮箱|None
    """
    _mail = re.match(r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$', mail)
    # 华科学号邮箱: [A-Za-z]\d{9}@hust.edu.cn
    # 华科一般邮箱: ^[A-Za-z0-9]+@hust.edu.cn
    # 不知道华科邮箱除了这些还有没有什么规则，测试的时候为了方便用的是普通邮箱的正则
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
        return _code==code

def login_or_register(_mail):
    _mail = encrypt_data(_mail) # 加密mail信息
    user_login = User.query.filter_by(mail = _mail).first()
    if user_login: #用户存在则直接返回
        user = User.query.filter_by(id=user_login.id).first()
        return user
    else:
        try:
            new_user = User(mail=_mail, user_group=0)
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            return None
        return new_user