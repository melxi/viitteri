from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
import os

def add_tweet(post, user_id):
    print(user_id)

    try:
        sql = """INSERT INTO tweets(post, user_id)
                 VALUES (:post, :user_id)"""
        db.session.execute(sql, {"post": post, "user_id": user_id})
        db.session.commit()
    except:
        return False

def get_tweets(user_id):
    sql = "SELECT * FROM tweets WHERE user_id=:user_id"
    result = db.session.execute(sql, {"user_id": user_id})
    tweets = result.fetchall()

    if not tweets:
        return False

    return tweets