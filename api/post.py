'''
树洞主体功能api
'''
from flask import Blueprint, request, jsonify, current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from api import api_bp

from .extensions import db
from .models import User, Post, Comments
from .decorator import token_required
from .enc import encrypt_data

# 发送树洞

@api_bp.route('/newPost', methods=["POST"])
@token_required
def newPost():
    try:
        token = request.headers["token"]
        s = Serializer(current_app.config["SECRET_KEY"])
        user_id = s.loads(token)["id"]

        request_data = request.get_json(force=True)
        title = request_data.get("title")
        content = request_data.get("content")
        post = Post(title=title, content=content)

        db.session.add(post)
        user = User.query.filter_by(id=user_id).first()
        post.author = encrypt_data(str(user.mail) + "|" + str(post.id))
        # post.author = encrypt_data(str(user_id) + "|" + str(post.id))
        # 此处有一隐患，若数据库被脱，理论上攻击者只要用公钥穷举user_id+"|"+post.id产生一个表即可，而user_id是非常小且有规律的
        # 改进v1：改成post.author = encrypt_data(str(user.mail) + "|" + str(post.id))
        # user.mail是经过一次RSA加密的，再来一次RSA加密
        # 根据华科邮箱规定：“别名最小长度3位，最大长度13位，必须以英文字母开头，允许使用数字、下划线，大写字母会自动转为小写！ 输入的别名不能包含域名！”
        # 即华科邮箱共有175911106378280941798种可能，经过估计，两次(mail字段也是使用RSA加密的)RSA计算在5ms左右，
        # 即尝试爆破需要175911106378280941798*5/1000/60/60/24/365约为27890522954年，即便算力提升上亿倍，仍然可认为是安全的。
        db.session.commit()
        return jsonify({"status": "success", "post_id": post.id})
    except Exception as e:
        return jsonify({"status": "failure"})

@api_bp.route('/newCoursePost', methods=["POST"])
@token_required
def newCoursePost():
    try:
        token = request.headers["token"]
        s = Serializer(current_app.config["SECRET_KEY"])
        user_id = s.loads(token)["id"]

        request_data = request.get_json(force=True)
        title = request_data.get("title")
        content = request_data.get("content") #选修课的数据用json格式存在content里面
        post = Post(title=title, content=content,kind = 1)
        post.author = encrypt_data(str(user_id)+"|"+str(post.id))
        db.session.add(post)
        db.session.commit()
        return jsonify({"status": "success", "post_id": post.id})
    except Exception as e:
        print(e)
        return jsonify({"status": "failure"})

# 获取树洞

@api_bp.route('/getPost/<post_id>', methods=["GET"])
@token_required
def getPost(post_id):
    post = Post.query.get_or_404(post_id)
    if (post.status==1):
        return_json = jsonify(
            {
                "status": "success",
                "title": post.title,
                "content": post.content,
                "kind": post.kind
            }
        )
    else:
        return_json = jsonify(
            {
                "status": "failure",
                "message":"banned"
            }
        )
    return return_json

# 评论

@api_bp.route('/comment/post/<post_id>', methods=["POST"])
@token_required
def commentPost(post_id):
    try:
        token = request.headers["token"]
        s = Serializer(current_app.config["SECRET_KEY"])
        user_id = s.loads(token)["id"]

        request_data = request.get_json(force=True)
        body = request_data.get("body")
        post = Post.query.filter_by(id=post_id).first()
        comment = Comments(body=body,post = post)
        
        db.session.add(comment)
        user = User.query.filter_by(id=user_id).first()
        comment.author = encrypt_data(str(user.mail)+"|"+str(comment.id))
        db.session.commit()
        return jsonify({"status": "success", "id": comment.id})
    except Exception as e:
        return jsonify({"status": "failure"})

@api_bp.route('/comment/comment/<comment_id>', methods=["POST"])
@token_required
def commentComment(comment_id):
    try:
        token = request.headers["token"]
        s = Serializer(current_app.config["SECRET_KEY"])
        user_id = s.loads(token)["id"]

        request_data = request.get_json(force=True)
        body = request_data.get("body")
        to_comment = Comments.query.filter_by(id=comment_id).first()
        
        comment = Comments(body=body,replied=to_comment)
        db.session.add(comment)

        user = User.query.filter_by(id=user_id).first()
        comment.author = encrypt_data(str(user.mail)+"|"+str(comment.id))
        db.session.commit()
        return jsonify({"status": "success", "id": comment.id})
    except Exception as e:
        return jsonify({"status": "failure"})

#获取评论
@api_bp.route('/comment/post/<post_id>', methods=["GET"])
@token_required
def get_comment_post(post_id):
    try:
        comment = Comments.query.filter_by(post_id=post_id)
        return_json = {}
        for index, item in enumerate(comment):
            if item.status == 0:
                continue
            return_json[str(index)] = {
                "id" : item.id,
                "body": item.body,
                "timestamps": item.timestamps,
                "replied_id": item.replied_id,
                "replies": [replie.id for replie in item.replies]
            }
        return jsonify({"status": "success","data":return_json})
    except Exception as e:
        return jsonify({"status": "failure"})

@api_bp.route('/comment/comment/<comment_id>', methods=["GET"])
@token_required
def get_comment_comment(comment_id):
    try:
        comment = Comments.query.filter_by(id=comment_id)
        return_json = {}
        for index, item in enumerate(comment):
            if item.status == 0:
                continue
            return_json[str(index)] = {
                "id" : item.id,
                "body": item.body,
                "timestamps": item.timestamps,
                "replied_id": item.replied_id,
                "replies": [replie.id for replie in item.replies]
            }
        return jsonify({"status": "success","data":return_json})
    except Exception as e:
        return jsonify({"status": "failure"})