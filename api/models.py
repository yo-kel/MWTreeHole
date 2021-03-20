from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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