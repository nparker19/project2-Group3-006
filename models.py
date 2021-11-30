from app import db
from flask_login import UserMixin
import os


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80))

    def __repr__(self):
        return f"<User {self.email}>"

    def get_username(self):
        return self.email


if os.getenv("DATABASE_URL") is not None:  # so our unit tests run in GitHub
    db.create_all()
