from flask import Flask
from flask_sqlalchemy import SQLAlchemy
server = Flask(__name__)
db = SQLAlchemy(server)

class Tweety(db.Model):
    __tablename__ = 'tweety'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(320))

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime)

db.create_all()