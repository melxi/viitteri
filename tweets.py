from db import db

def add_tweet(post, user_id):
    try:
        sql = """INSERT INTO tweets(post, user_id)
                 VALUES (:post, :user_id)"""
        db.session.execute(sql, {"post": post, "user_id": user_id})
        db.session.commit()
    except:
        return False

def get_tweets(user_id):
    sql = "SELECT * FROM tweets WHERE user_id=:user_id ORDER BY created_at DESC"
    result = db.session.execute(sql, {"user_id": user_id})
    tweets = result.fetchall()

    if not tweets:
        return False

    return tweets

def get_tweet(tweet_id):
    sql = """SELECT tw.post, tw.total_likes, tw.total_replies, tw.created_at, us.username  
             FROM tweets AS tw
             INNER JOIN users AS us ON tw.user_id = us.user_id 
             WHERE tweet_id=:tweet_id"""
    result = db.session.execute(sql, {"tweet_id": tweet_id})
    tweet = result.fetchone()

    if not tweet:
        return False

    return tweet