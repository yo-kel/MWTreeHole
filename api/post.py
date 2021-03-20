from .models import User, Post, Comments
from flask import Blueprint, request, jsonify, current_app
from .models import db, token_required
from api import api_bp
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@api_bp.route('/new_post', methods=["GET", "POST"])
@token_required
def new_post():
    try:
        token = request.headers["token"]
        
        s = Serializer(current_app.config["SECRET_KEY"])
        author_id = s.loads(token)["id"]
        request_data = request.get_json(force=True)
        title = request_data.get("title")
        content = request_data.get("content")
        post = Post(title=title, content=content, author_id=author_id)
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
    return_json = jsonify(
        {
            "status": "success",
            "title": post.title,
            "content": post.content,
        }
    )
    return return_json