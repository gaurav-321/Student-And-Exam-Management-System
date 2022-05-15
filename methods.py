from app import db
from models import User
from flask import session


def add_user(uname, pwd):
    user = User(uname, pwd)
    db.session.add(user)
    db.session.commit()


def login_user(username):
    session['logged_in'] = True
    session['username'] = username


def user_logged():
    if "logged_in" in session.keys() and session['logged_in'] is True:
        return True
    else:
        return False
