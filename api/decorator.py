'''
实现权限分级的装饰器
'''
import functools

from flask import current_app, jsonify, request
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from .models import User

def token_required(view_func):
    @functools.wraps(view_func)
    def verify_token(*args,**kwargs):
        try:
            token = request.headers["token"]
        except Exception as e:
            return jsonify(code = 4103,msg = 'missing token')
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            s.loads(token)
        except Exception:
            return jsonify(code = 4101,msg = "token outdate")
        return view_func(*args,**kwargs)
    return verify_token

def su_required(view_func):
    @functools.wraps(view_func)
    def verify_su(*args, **kwargs):
        #使用时配合token_required装饰器使用
        s = Serializer(current_app.config["SECRET_KEY"])
        token = request.headers["token"]
        info = s.loads(token)
        if User.query.filter_by(id=info["id"]).first().user_group != 6:
            return jsonify(code=4103, msg='unauthorized operation')
        return view_func(*args,**kwargs)
    return verify_su

def admin_required(view_func):
    @functools.wraps(view_func)
    def verify_admin(*args, **kwargs):
        #使用时配合token_required装饰器使用
        s = Serializer(current_app.config["SECRET_KEY"])
        token = request.headers["token"]
        info = s.loads(token)
        if User.query.filter_by(id=info["id"]).first().user_group <5 :
            return jsonify(code=4103, msg='unauthorized operation')
        return view_func(*args,**kwargs)
    return verify_admin
