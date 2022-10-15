import os
from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from db import db

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
    session["logged_in"] = True
    return True

def logout():
    del session["user_id"]
    del session["username"]
    del session["user_role"]
    session["logged_in"] = False

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

def get_user():
    sql = """SELECT us.username, TO_CHAR(us.created_at, 'Month YYYY') AS joined,
            (SELECT COUNT(tw.tweet_id) FROM tweets AS tw WHERE user_id=:user_id) AS total_tweets,
            (SELECT COUNT(fw.followee_id) FROM followees AS fw WHERE user_id=:user_id) AS total_followees,
            (SELECT COUNT(fl.follower_id) FROM followers AS fl WHERE user_id=:user_id) AS total_followers
            FROM users AS us
            WHERE us.user_id=:user_id"""
    result = db.session.execute(sql, {"user_id": user_id()})
    user = result.fetchone()

    return user

def follow_user(user_id, followee_id):
    sql = """SELECT user_id, followee_id
            FROM followees 
            WHERE user_id=:user_id AND followee_id=:followee_id"""
    result = db.session.execute(sql, {"user_id": user_id, "followee_id":followee_id})
    followee = result.fetchone()

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
    return True

def get_followees():
    sql = """SELECT us.user_id, us.username
            FROM followees AS fw
            INNER JOIN users AS us ON us.user_id = fw.followee_id
            WHERE fw.user_id=:user_id"""
    result = db.session.execute(sql, {"user_id": user_id()})
    followees = result.fetchall()

    return followees

# get followers and those who you follow
def get_followers():
    sql = """SELECT us.username, fl.user_id, fl.follower_id, fw.user_id, fw.followee_id
            FROM followers AS fl
            LEFT JOIN users AS us ON us.user_id = fl.follower_id
            LEFT JOIN followees AS fw ON fw.user_id = fl.user_id AND fl.follower_id = fw.followee_id
            WHERE fl.user_id=:user_id"""
    result = db.session.execute(sql, {"user_id": user_id()})
    followers = result.fetchall()

    return followers
