from main_app import db ,migrate,login_manager
from flask_login import UserMixin, AnonymousUserMixin
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import event
from flask import current_app
import os


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column("image", db.String(150), default="doc.png")
    fname = db.Column(db.String(72), nullable=False)
    lname = db.Column(db.String(72), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    pwd = db.Column(db.String(72), nullable=False, unique=True)
    email = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    sex = db.Column(db.String(20), nullable=False)
    speciality = db.Column(db.String(20), default="Doctor")
    status = db.Column(db.Boolean, default=False)
        
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

