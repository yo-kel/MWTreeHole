import functools

from flask import Flask

from config import Config

from api import api_bp
from api.extensions import db

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

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
