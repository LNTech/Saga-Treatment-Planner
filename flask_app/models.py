# models.py
from extensions import db
from flask_login import UserMixin

class Customer(db.Model):
    __tablename__ = "Customers"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    sites = db.relationship('Site', backref='customer', lazy=True)

class Site(db.Model):
    __tablename__ = "Sites"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, unique=False, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('Customers.id'))
    fields = db.relationship('Field', backref='site', lazy=True)

class Field(db.Model):
    __tablename__ = "Fields"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, unique=False, nullable=False)
    site_id = db.Column(db.Integer, db.ForeignKey('Sites.id'), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)

class User(UserMixin, db.Model):
    __tablename__ = "Users"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String, unique=True, nullable=False) # Public ID to protect against id enumeration
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=False, nullable=False)
    privileges = db.Column(db.String(5), unique=False, nullable=False) # admin, user


class Invite(db.Model):
    __tablename__ = "Invites"

    id = db.Column(db.Integer, primary_key=True)
    invite_code = db.Column(db.String, unique=True, nullable=False)
    is_redeemed = db.Column(db.Boolean, default=False, unique=False, nullable=False)