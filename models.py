from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    cpf = db.Column(db.String(14), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    residence_id = db.Column(db.Integer, db.ForeignKey('residence.id'))

class Residence(db.Model):
    __tablename__ = 'residences'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(150), nullable=False)
    size_sqm = db.Column(db.Float, nullable=False)
    residents = db.relationship('User', backref='residence', lazy=True)
    pets = db.relationship('Pet', backref='residence', lazy=True)
