from db import db
import tweets

def add_like(tweet_id, user_id):
    if not has_liked(tweet_id, user_id):
        try:
            sql = """INSERT INTO likes(tweet_id, user_id)
                    VALUES (:tweet_id, :user_id)"""
            db.session.execute(sql, {"tweet_id": tweet_id, "user_id": user_id})
            db.session.commit()
        except:
            return False
    return True

def remove_like(tweet_id, user_id):
    if has_liked(tweet_id, user_id):
        try:
            sql = "DELETE FROM likes WHERE tweet_id=:tweet_id AND user_id=:user_id"
            db.session.execute(sql, {"tweet_id": tweet_id, "user_id": user_id})
            db.session.commit()
        except:
            return False
    return True

def get_likers(tweet_id):
    sql = """SELECT user_id, COUNT(like_id)
            FROM likes WHERE tweet_id=:tweet_id
            GROUP BY user_id"""
    result = db.session.execute(sql, {"tweet_id": tweet_id})
    likes = result.fetchall()

    if not likes:
        return False
    return likes

def has_liked(tweet_id, user_id):
    sql = """SELECT
                CASE WHEN EXISTS
                    (SELECT * FROM likes WHERE tweet_id=:tweet_id AND user_id=:user_id)
                THEN 'True' ELSE 'False' END AS liked"""
    result = db.session.execute(sql, {"tweet_id": tweet_id, "user_id": user_id})
    liked = result.fetchone()


    if liked and liked['liked'] == 'True':
        return True
    return False
