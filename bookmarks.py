from db import db

def add_bookmark(tweet_id, user_id):
    if not has_bookmarked(tweet_id, user_id):
        try:
            sql = """INSERT INTO bookmarks(tweet_id, user_id)
                    VALUES (:tweet_id, :user_id)"""
            db.session.execute(sql, {"tweet_id": tweet_id, "user_id": user_id})
            db.session.commit()
        except:
            return False
    return True

def remove_bookmark(tweet_id, user_id):
    if has_bookmarked(tweet_id, user_id):
        try:
            sql = "DELETE FROM bookmarks WHERE tweet_id=:tweet_id AND user_id=:user_id"
            db.session.execute(sql, {"tweet_id": tweet_id, "user_id": user_id})
            db.session.commit()
        except:
            return False
    return True

def has_bookmarked(tweet_id, user_id):
    sql = """SELECT
                CASE WHEN EXISTS
                    (SELECT * FROM bookmarks WHERE tweet_id=:tweet_id AND user_id=:user_id)
                THEN 'True' ELSE 'False' END AS bookmarked"""
    result = db.session.execute(sql, {"tweet_id": tweet_id, "user_id": user_id})
    bookmarked = result.fetchone()

    if bookmarked and bookmarked['bookmarked'] == 'True':
        return True
    return False

def get_bookmarks(user_id):
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
             (SELECT COUNT(lk.user_id) FROM likes AS lk WHERE tweet_id = tw.tweet_id) AS total_likes,
             (SELECT COUNT(rp.tweet_id) FROM replies AS rp WHERE tweet_id = tw.tweet_id) AS total_replies,
             (SELECT
                CASE WHEN EXISTS
                    (SELECT * FROM likes WHERE tweet_id = tw.tweet_id AND user_id=:user_id)
                THEN 'True' ELSE 'False' END) AS liked,
             (SELECT
                CASE WHEN EXISTS
                    (SELECT * FROM bookmarks WHERE tweet_id = tw.tweet_id AND user_id=:user_id)
                THEN 'True' ELSE 'False' END) AS bookmarked,
             (SELECT us.username FROM users AS us WHERE tw.user_id = us.user_id) AS username
             FROM bookmarks AS bk
             LEFT JOIN tweets AS tw ON bk.tweet_id = tw.tweet_id
             WHERE bk.user_id=:user_id
             GROUP BY tw.tweet_id
             ORDER BY created_at DESC"""
    result = db.session.execute(sql, {"user_id": user_id})
    tweets = result.fetchall()

    if not tweets:
        return False
    return tweets