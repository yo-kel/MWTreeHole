from app import create_app, db
from api.models import User, Post, Comments

app = create_app()
with app.app_context():
    db.create_all()