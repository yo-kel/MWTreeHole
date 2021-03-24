import datetime

from .extensions import db

class User(db.Model):
    '''
    用户表
    '''
    __tablename__ = 't_user'
    id = db.Column(db.Integer, primary_key = True)
    mail = db.Column(db.Text) #邮箱,使用RSA算法加密
    user_group = db.Column(db.Integer, default=0)  #用户组,0为普通用户,6为管理员
    public_key = db.Column(db.Text) #管理员的public_key
    token = db.Column(db.String(128)) #token字段，暂时没用

    follow_post = db.Column(db.Text) #关注的帖子

    def generate_auth_token(self, expiration = 600): #生成token
        s = Serializer(current_app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({'id': self.id})

class Post(db.Model):
    __tablename__ = 't_post'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    title = db.Column(db.String(100), index=True, nullable=False) #标题
    content = db.Column(db.Text, nullable=False)  #内容
    timestamps = db.Column(db.DateTime, default=datetime.datetime.now) #发表时间
    kind = db.Column(db.Integer,default = 0) #文章类别: 0 树洞 1 爱选修
    status = db.Column(db.Integer, default = 1) #状态 1为正常，0为封禁
    operator = db.Column(db.Integer)

    author = db.Column(db.Text) #作者信息,使用RSA算法保证安全
    comments = db.relationship('Comments', back_populates='post', cascade='all') #一级评论的id



class Comments(db.Model):
    __tablename__ = 't_comments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    body = db.Column(db.Text) #评论内容
    timestamps = db.Column(db.DateTime, default=datetime.datetime.now) #评论时间

    author = db.Column(db.Text) #作者信息,使用RSA算法保证安全
    
    status = db.Column(db.Integer, default = 1) #状态 1为正常，0为封禁
    operator = db.Column(db.Integer)
    
    replied_id = db.Column(db.Integer, db.ForeignKey('t_comments.id')) #回复的评论的id
    post_id = db.Column(db.Integer, db.ForeignKey('t_post.id')) #所属树洞的id,一级评论方有此字段

    post = db.relationship('Post', back_populates='comments') #所属的树洞
    replies = db.relationship('Comments', back_populates='replied', cascade='all') #回复自己的
    replied = db.relationship('Comments', back_populates='replies', remote_side=[id]) #回复的
