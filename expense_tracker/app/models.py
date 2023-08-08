from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    # other fields

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # other fields

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # other fields
