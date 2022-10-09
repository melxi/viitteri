from db import db

def add_tweet(post, user_id):
    try:
        sql = """INSERT INTO tweets(post, user_id)
                 VALUES (:post, :user_id) RETURNING tweet_id"""
        result = db.session.execute(sql, {"post": post, "user_id": user_id})
        db.session.commit()
        return result.fetchone()[0]
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
    sql = """SELECT tw.tweet_id, tw.post, tw.total_likes, tw.created_at, us.username,
                (CASE
                    WHEN (DATE_PART('year', now()) - DATE_PART('year', tw.created_at)) > 1
                        THEN TO_CHAR(tw.created_at, 'Mon DD YYYY')
                    WHEN (DATE_PART('year', now()) - DATE_PART('year', tw.created_at)) = 1
                        THEN TO_CHAR(tw.created_at, 'Mon DD YYYY')
                    WHEN DATE_PART('day', now() - tw.created_at) > 1
                        THEN TO_CHAR(tw.created_at, 'Mon DD')
                    WHEN DATE_PART('day', now() - tw.created_at) = 1
                        THEN TO_CHAR(tw.created_at, 'Mon DD')
                    WHEN ((DATE_PART('day', now() - tw.created_at) * 24) + (DATE_PART('hour', now() - tw.created_at))) > 1
                        THEN CONCAT(((DATE_PART('day', now() - tw.created_at) * 24) + (DATE_PART('hour', now() - tw.created_at))), ' hours ago')
                    WHEN ((DATE_PART('day', now() - tw.created_at) * 24) + (DATE_PART('hour', now() - tw.created_at))) = 1
                        THEN CONCAT(((DATE_PART('day', now() - tw.created_at) * 24) + (DATE_PART('hour', now() - tw.created_at))), ' hour ago')
                    WHEN ((DATE_PART('day', now() - tw.created_at) * 24) + ((DATE_PART('hour', now() - tw.created_at)) * 60) + (DATE_PART('minute', now() - tw.created_at))) > 1
                        THEN CONCAT(((DATE_PART('day', now() - tw.created_at) * 24) + ((DATE_PART('hour', now() - tw.created_at)) * 60) + (DATE_PART('minute', now() - tw.created_at))), ' minutes ago')
                    WHEN ((DATE_PART('day', now() - tw.created_at) * 24) + ((DATE_PART('hour', now() - tw.created_at)) * 60) + (DATE_PART('minute', now() - tw.created_at))) = 1
                        THEN CONCAT(((DATE_PART('day', now() - tw.created_at) * 24) + ((DATE_PART('hour', now() - tw.created_at)) * 60) + (DATE_PART('minute', now() - tw.created_at))), ' minute ago')
                ELSE 'just now'
                END) AS created_at,
             (SELECT COUNT(rp.tweet_id) FROM replies AS rp WHERE tweet_id=:tweet_id) AS total_replies,
             (SELECT us.username 
             FROM tweets AS tw INNER JOIN users AS us ON tw.user_id = us.user_id 
             WHERE tw.tweet_id=(SELECT rp.tweet_id FROM replies AS rp WHERE reply_id=:tweet_id)) AS reply_to
             FROM tweets AS tw
             INNER JOIN users AS us ON tw.user_id = us.user_id 
             WHERE tw.tweet_id=:tweet_id"""
    result = db.session.execute(sql, {"tweet_id": tweet_id})
    tweet = result.fetchone()

    if not tweet:
        return False

    return tweet