from flask import Flask, jsonify
from config import Config
from flask_mail import Message, Mail
from api import auth
import api.models
from api.models import db

app=Flask(__name__)
app.config.from_object(Config)

mail_host = Mail()

def creatapp():
    db.init_app(app)
    app.register_blueprint(auth.api_bp)
    mail_host.init_app(app)
    return app
db.create_all(app=creatapp())

creatapp()
@app.route('/')
def index():
    return "Hello, World!"


if __name__ == '__main__':
    app.run(debug=True)
