from flask_sqlalchemy import SQLAlchemy
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app,jsonify,request
import functools
import datetime
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
    __tablename__ = 't_user'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(32), index = True)
    mail = db.Column(db.String(128))
    user_group = db.Column(db.Integer)
    token = db.Column(db.String(128))

    comments = db.relationship('Comments', back_populates='author', cascade='all')

    def generate_auth_token(self, expiration = 600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({'id': self.id})

class Post(db.Model):
    __tablename__ = 't_post'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    title = db.Column(db.String(100), index=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.Integer, default = 1)

    author_id = db.Column(db.Integer, db.ForeignKey('t_user.id'))
    comments = db.relationship('Comments', back_populates='post', cascade='all')



class Comments(db.Model):
    __tablename__ = 't_comments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    body = db.Column(db.Text)
    timestamps = db.Column(db.DateTime, default=datetime.datetime.now)

    author_id = db.Column(db.Integer, db.ForeignKey('t_user.id'))
    
    replied_id = db.Column(db.Integer, db.ForeignKey('t_comments.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('t_post.id'))

    post = db.relationship('Post', back_populates='comments')
    author = db.relationship('User', back_populates='comments')
    replies = db.relationship('Comments', back_populates='replied', cascade='all')
    replied = db.relationship('Comments', back_populates='replies', remote_side=[id])
