from flask import Flask, url_for, redirect, render_template, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user
from flask_security.utils import encrypt_password
import datetime
from database import db



# Define models
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime(), default=datetime.datetime.now)
    
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        return self.email


def initialize(app):
	app.config['SECURITY_PASSWORD_HASH'] = 'sha512_crypt'
	app.config['SECURITY_PASSWORD_SALT'] = '$817djwmfld0k*!MJAmdlswwqzpzdneia'
	
	user_datastore = SQLAlchemyUserDatastore(db, User, Role)
	security_ctx = Security(app, user_datastore)

	return (security_ctx, user_datastore)

def _preload():
	db.create_all()
	roles = _role_preload()
	_user_preload(roles)

def _role_preload():
	user_role = Role(name='user', description='A normal user with basic rights')
	superuser_role = Role(name='superuser', description='Allowed to do anything')
	db.session.add(user_role)
	db.session.add(superuser_role)
	db.session.commit()

	return {'user': user_role, 'superuser':superuser_role}

def _user_preload(roles):
	pdk = User(email='philip.dekeulenaer@gmail.com', first_name='Philip', last_name='De Keulenaer')
	pdk.roles = roles.values()
	pdk.password = encrypt_password('playstation22')
	db.session.add(pdk)
	db.session.commit()

