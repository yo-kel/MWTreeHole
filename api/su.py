from .models import User, Post, Comments
from flask import Blueprint, request, jsonify, current_app
from .models import db, su_required, token_required,admin_required
from api import api_bp
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from .enc import encrypt_data

@api_bp.route('/sudo/<user_id>', methods=["GET", "POST"])
@su_required
def sudo_user():  #用户提权到管理员的函数,验证enc参数是否由su签发
    try:
        request_data = request.get_json(force=True)
        enc_id = request_data.get("enc_id")
        if not rsa_signature_decode(str(user_id), str(enc_id)):
            return jsonify(code=4102, msg='wrong enc')

        user = User.query.filter_by(id=user_id).first()
        user.user_group = 5
        db.session.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        print(e)
        return jsonify({"status": "failure"})

@api_bp.route('/ban_post/<post_id>', methods=["GET", "POST"])
@admin_required
def ban_post(post_id):
    def ban_sub_comment(comments):
        for _comment in comments:
            _comment.status = 0
            _comment.operator = user_id
            ban_sub_comment(_comment.replies)
    try:
        token = request.headers["token"]
        s = Serializer(current_app.config["SECRET_KEY"])
        user_id = s.loads(token)["id"]

        post = Post.query.filter_by(id=post_id).first()
        post.status = 0
        post.operator = user_id
        ban_sub_comment(post.comments) #递归删除子评论
                    
        db.session.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        print(e)
        return jsonify({"status": "failure"})

@api_bp.route('/ban_comment/<comment_id>', methods=["GET", "POST"])
@admin_required
def ban_comment(comment_id):
    def ban_sub_comment(comments):
        for _comment in comments:
            _comment.status = 0
            _comment.operator = user_id
            ban_sub_comment(_comment.replies)
    try:
        token = request.headers["token"]
        s = Serializer(current_app.config["SECRET_KEY"])
        user_id = s.loads(token)["id"]

        comment = Comments.query.filter_by(id=comment_id).first()
        comment.status = 0
        comment.operator = user_id
        ban_sub_comment(comment.comments) #递归删除子评论
        db.session.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        print(e)
        return jsonify({"status": "failure"})
        

@api_bp.route('/get_author/post/<post_id>', methods=["GET", "POST"])
@su_required
def get_post_author(post_id):
    post = Post.query.filter_by(id=post_id).first()
    return jsonify({"status": "success", "author": post.author})

@api_bp.route('/get_author/comment/<comment_id>', methods=["GET", "POST"])
@su_required
def get_comment_author(comment_id):
    comment = Comments.query.filter_by(id=comment_id).first()
    return jsonify({"status": "success", "author": comment.author})

@api_bp.route('/sudo_test', methods=["GET", "POST"])
@token_required
def sudo_test():
    user = User.query.filter_by(id=1).first()
    user.user_group = 6
    db.session.commit()
    return "ok"