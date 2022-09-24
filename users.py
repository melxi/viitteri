from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
import os

def login(username, password):
    sql = "SELECT id, password FROM users where username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()

    if not user:
        return False
    if not check_password_hash(user[0], password):
        return False

    session["user_id"] = user[1]
    session["username"] = username
    session["csrf_token"] = os.urandom(16).hex()
    
    return True

def logout():
    del session["user_id"]
    del session ["username"]

def signup(username, password):
    hash_value = generate_password_hash(password)
    print(username)
    print(password)
    try:
        sql = """INSERT INTO users(username, password)
                 VALUES (:username, :password)"""
        db.session.execute(sql, {"username": username, "password": hash_value})
        db.session.commit()
    except:
        return False

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)