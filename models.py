from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime


db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    type = db.Column(db.String(20))
    category = db.Column(db.String(100))
    amount = db.Column(db.Float)
    description = db.Column(db.String(200))

    date = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))