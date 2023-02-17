import re

from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager
from flask_login import UserMixin
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.orm import validates

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    phone_number = db.Column(db.String(120), nullable=True)
    roles = db.relationship('Role', secondary='user_roles', lazy='subquery', backref=db.backref('users', lazy=True))

    @validates('phone_number')
    def do_validation(self, key, field):
        if not re.fullmatch(re.compile(r'^(?:\+?44)?[07]\d{9,13}$'), field):
            raise ValueError('Not a valid phone number.')
        return field

    def __init__(self, email, password, first_name, last_name, phone_number=None):
        self.email = email
        self.password = generate_password_hash(password).decode("utf-8")
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number

    def check_password(self, password):
        return check_password_hash(self.password, password)


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True

    id = ma.auto_field()
    email = ma.auto_field()
    first_name = ma.auto_field()
    last_name = ma.auto_field()
    phone_number = ma.auto_field()


class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False)


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


class RoleSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Role
        fields = ['name']


class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))


@event.listens_for(Role.__table__, 'after_create')
def create_roles(target, connection, **kwargs):
    connection.execute(target.insert(), ({'name': 'Clown'}, {'name': 'Client'}, {'name': 'Troupe Leader'}))


