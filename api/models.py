from flask_sqlalchemy import SQLAlchemy
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app,jsonify,request
import functools
db = SQLAlchemy()

def token_required(view_func):
    @functools.wraps(view_func)
    def verify_token(*args,**kwargs):
        try:
            #在请求头上拿到token
            token = request.headers["token"]
        except Exception as e:
            print(e)
            return jsonify(code = 4103,msg = 'missing token')
        
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            s.loads(token)
        except Exception:
            return jsonify(code = 4101,msg = "token outdate")

        return view_func(*args,**kwargs)

    return verify_token

class User(db.Model):
    '''
    用户表
    '''
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(32), index = True)
    mail = db.Column(db.String(128))
    user_group = db.Column(db.Integer)
    token = db.Column(db.String(36))

    def generate_auth_token(self, expiration = 600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.id })