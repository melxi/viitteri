from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
import os

def login(username, password):
    sql = "SELECT user_id, password, role FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()

    if not user:
        return False
    if not check_password_hash(user[1], password):
        return False

    session["user_id"] = user[0]
    session["username"] = username
    session["user_role"] = user[2]
    session["csrf_token"] = os.urandom(16).hex()
    
    return True

def logout():
    del session["user_id"]
    del session["username"]
    del session["user_role"]

def signup(username, password):
    password_hash = generate_password_hash(password)
    
    try:
        sql = """INSERT INTO users(username, password)
                 VALUES (:username, :password)"""
        db.session.execute(sql, {"username":username, "password":password_hash})
        db.session.commit()
    except:
        return False

    return login(username, password)

def user_id():
    return session.get("user_id", 0)

def require_role(role):
    if role > session.get("user_role", 0):
        return False
    else:
        return True

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    

def get_users():
    sql = """SELECT us.user_id, us.username, fw.followee_id, fl.follower_id 
             FROM users AS us
             FULL OUTER JOIN followees AS fw ON us.user_id = fw.user_id 
             FULL OUTER JOIN followers AS fl ON us.user_id = fl.user_id
             WHERE us.user_id!=:user_id"""
    result = db.session.execute(sql, {"user_id": user_id()})
    users = result.fetchall()

    return users

def follow_user(user_id, followee_id):
    print('user_id', user_id)
    print('followee_id', followee_id)
    sql = "SELECT user_id, followee_id FROM followees WHERE user_id=:user_id AND followee_id=:followee_id"
    result = db.session.execute(sql, {"user_id": user_id, "followee_id":followee_id})
    followee = result.fetchone()

    print('followee', followee)
    if not followee:
        try:
            sql = """INSERT INTO followees(user_id, followee_id)
                    VALUES (:user_id, :followee_id)"""
            db.session.execute(sql, {"user_id":user_id, "followee_id":followee_id})
            db.session.commit()

            sql = """INSERT INTO followers(user_id, follower_id)
                    VALUES (:user_id, :follower_id)"""
            db.session.execute(sql, {"user_id":followee_id, "follower_id":user_id})
            db.session.commit()
        except:
            return False

    print('already following')
    return True