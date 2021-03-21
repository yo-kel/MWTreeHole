from flask import Flask, jsonify, redirect, url_for,send_from_directory,request
from config import Config
from flask_mail import Message, Mail
from api import auth
import api.models
from api.models import db
from api.models import token_required
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import functools

app=Flask(__name__,static_url_path='')
app.config.from_object(Config)

mail_host = Mail()

def creatapp():
    db.init_app(app)
    app.register_blueprint(auth.api_bp)
    mail_host.init_app(app)
    return app
db.create_all(app=creatapp())

#creatapp()

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


if __name__ == '__main__':
    app.run(debug=True)
