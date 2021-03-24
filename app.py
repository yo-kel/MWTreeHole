import functools

from flask import Flask, jsonify, redirect, url_for,send_from_directory,request
from flask_mail import Message, Mail
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from config import Config

from api import api_bp
from api.extensions import db
from api.models import User, Post, Comments

def create_app():
    app=Flask(__name__,static_url_path='')
    app.config.from_object(Config)
    register_extensions(app)
    register_blueprints(app)
    return app

def register_extensions(app):
    db.init_app(app)

def register_blueprints(app):
    app.register_blueprint(api_bp)

# mail_host = Mail()

# def creatapp():
# db.init_app(app)

# mail_host.init_app(app)
# db.create_all(app)
    # return app
#

'''
def login_required(view_func):
    @functools.wraps(view_func)
    def verify_login(*args, **kwargs):
        try:
            token = request.cookies.get('token')
        except Exception as e:
            print(e)
            return redirect(url_for("login"))
        
        s = Serializer(app.config["SECRET_KEY"])
        try:
            s.loads(token)
        except Exception:
            return redirect(url_for("login"))
        
        return view_func(*args,**kwargs)
    return verify_login

@app.route('/')
@app.route('/index')
@login_required
def index():
    return send_from_directory("layout","index.html")

@app.route('/login')
def login():
    return send_from_directory("layout","login.html")
'''

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
