from flask import Blueprint, request, jsonify, current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from api import api_bp

from .extensions import db
from .models import User, Post, Comments
from .decorator import token_required
from .enc import encrypt_data

@api_bp.route('/new_post', methods=["GET", "POST"])
@token_required
def new_post():
    try:
        token = request.headers["token"]
        s = Serializer(current_app.config["SECRET_KEY"])
        user_id = s.loads(token)["id"]

        request_data = request.get_json(force=True)
        title = request_data.get("title")
        content = request_data.get("content")
        post = Post(title=title, content=content)
        post.author = encrypt_data(str(user_id)+"|"+str(post.id))
        db.session.add(post)
        db.session.commit()
        return jsonify({"status": "success", "post_id": post.id})
    except Exception as e:
        print(e)
        return jsonify({"status": "failure"})

@api_bp.route('/new_post_course', methods=["GET", "POST"])
@token_required
def new_post_course():
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

@api_bp.route('/get_post/<post_id>', methods=["GET", "POST"])
@token_required
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    if (post.status==1):
        return_json = jsonify(
            {
                "status": "success",
                "title": post.title,
                "content": post.content
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

@api_bp.route('/comment/post/<post_id>', methods=["POST"])
@token_required
def comment_post(post_id):
    try:
        token = request.headers["token"]
        s = Serializer(current_app.config["SECRET_KEY"])
        user_id = s.loads(token)["id"]

        request_data = request.get_json(force=True)
        body = request_data.get("body")
        post = Post.query.filter_by(id=post_id).first()
        comment = Comments(body=body,post = post)
        
        comment.author = encrypt_data(str(user_id)+"|"+str(comment.id))
        db.session.add(comment)
        db.session.commit()
        return jsonify({"status": "success", "id": comment.id})
    except Exception as e:
        print(e)
        return jsonify({"status": "failure"})

@api_bp.route('/comment/comment/<comment_id>', methods=["POST"])
@token_required
def comment_comment(comment_id):
    try:
        token = request.headers["token"]
        s = Serializer(current_app.config["SECRET_KEY"])
        user_id = s.loads(token)["id"]

        request_data = request.get_json(force=True)
        body = request_data.get("body")
        to_comment = Comments.query.filter_by(id=comment_id).first()
        
        comment = Comments(body=body,replied=to_comment)

        comment.author = encrypt_data(str(user_id)+"|"+str(comment.id))
        db.session.add(comment)
        db.session.commit()
        return jsonify({"status": "success", "id": comment.id})
    except Exception as e:
        print(e)
        return jsonify({"status": "failure"})

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
        print(e)
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
        print(e)
        return jsonify({"status": "failure"})