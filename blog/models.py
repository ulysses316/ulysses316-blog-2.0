from . import db
from flask_login import UserMixin
import datetime

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    title = db.Column(db.TEXT, nullable=False)
    body = db.Column(db.TEXT, nullable=False)
    file = db.Column(db.TEXT, nullable=False)

class Workshop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    title = db.Column(db.TEXT, nullable=False)
    body = db.Column(db.TEXT, nullable=False)
    url = db.Column(db.TEXT,nullable=True)
    file = db.Column(db.TEXT, nullable=False)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    title = db.Column(db.TEXT, nullable=False)
    body = db.Column(db.TEXT, nullable=False)
    url = db.Column(db.TEXT, nullable=True)
    language = db.Column(db.String(25))
