from db import db
import tweets

def add_reply(tweet_id, user_id, post):
    reply_id = tweets.add_tweet(post, user_id)
    try:
        sql = """INSERT INTO replies(reply_id, tweet_id)
                 VALUES (:reply_id, :tweet_id)"""
        db.session.execute(sql, {"reply_id": reply_id, "tweet_id": tweet_id})
        db.session.commit()
    except:
        return False

def get_replies(tweet_id):
    sql = "SELECT * FROM replies WHERE tweet_id=:tweet_id"
    result = db.session.execute(sql, {"tweet_id": tweet_id})
    results = result.fetchall()

    if not results:
        return False

    replies = []
    for result in results:
        replies.append(tweets.get_tweet(result[0]))

    # Sort replies by datetime
    replies.sort(key=lambda reply: reply[4], reverse=True)

    return replies