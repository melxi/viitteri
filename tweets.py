from db import db
from flask import session
import users

def add_tweet(post, user_id):
    try:
        sql = """INSERT INTO tweets(post, user_id)
                 VALUES (:post, :user_id) RETURNING tweet_id"""
        result = db.session.execute(sql, {"post": post, "user_id": user_id})
        db.session.commit()
        return result.fetchone()[0]
    except:
        return False

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
             (SELECT COUNT(lk.user_id) FROM likes AS lk WHERE tweet_id = tw.tweet_id) AS total_likes,
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

def get_tweets(user_id):
    followees = users.get_followees(user_id)

    user_ids = [user_id]
    if followees:
        for followee in followees:
            user_ids.append(followee[0])

    sql = """SELECT tw.tweet_id, tw.post, tw.created_at, us.username,
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
             (SELECT COUNT(rp.tweet_id) FROM replies AS rp WHERE tweet_id = tw.tweet_id) AS total_replies,
             (SELECT COUNT(lk.user_id) FROM likes AS lk WHERE tweet_id = tw.tweet_id) AS total_likes,
             (SELECT
                CASE WHEN EXISTS
                    (SELECT * FROM likes WHERE tweet_id = tw.tweet_id AND user_id=:user_id)
                THEN 'True' ELSE 'False' END) AS liked
             FROM tweets AS tw
             INNER JOIN users AS us ON tw.user_id = us.user_id
             WHERE tw.user_id IN :user_ids ORDER BY tw.created_at DESC"""
    result = db.session.execute(sql, {"user_id": user_id, "user_ids": tuple(user_ids)})
    tweets = result.fetchall()
    return tweets

def get_recent_tweets(user_id):
    sql = """SELECT tw.tweet_id, tw.post,
                (CASE
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
             COUNT(lk.tweet_id) AS total_likes,
             COUNT(rp.tweet_id) AS total_replies,
             (SELECT
                CASE WHEN EXISTS
                    (SELECT * FROM likes WHERE tweet_id = tw.tweet_id AND user_id=:user_id)
                THEN 'True' ELSE 'False' END) AS liked,
             (SELECT us.username FROM users AS us WHERE tw.user_id = us.user_id) AS username
             FROM tweets AS tw
             LEFT JOIN likes AS lk ON tw.tweet_id = lk.tweet_id
             LEFT JOIN replies AS rp ON tw.tweet_id = rp.tweet_id
             WHERE created_at >= NOW() - '1 day'::INTERVAL
             GROUP BY tw.tweet_id
             ORDER BY total_likes DESC"""
    result = db.session.execute(sql, {"user_id": user_id})
    tweets = result.fetchall()

    if not tweets:
        return False
    return tweets