CREATE TABLE users(
    user_id SERIAL,
    username VARCHAR(20) NOT NULL,
    favorites_count INTEGER DEFAULT 0,
    password TEXT NOT NULL,
    role INTEGER DEFAULT 1,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(user_id)
);

CREATE TABLE tweets(
    tweet_id SERIAL,
    user_id INTEGER NOT NULL,
    post VARCHAR(280) NOT NULL,
    total_likes INTEGER DEFAULT 0,
    total_replies INTEGER DEFAULT 0,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(tweet_id),
    CONSTRAINT tw_users_fk
      FOREIGN KEY(user_id) 
	    REFERENCES users(user_id)
);

CREATE TABLE replies(
    reply_id SERIAL,
    user_id INTEGER NOT NULL,
    tweet_id INTEGER NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(reply_id),
    CONSTRAINT rp_users_fk
      FOREIGN KEY(user_id) 
	    REFERENCES users(user_id),
    CONSTRAINT rp_tweets_fk
      FOREIGN KEY(tweet_id) 
	    REFERENCES tweets(tweet_id)
);

CREATE TABLE followees(
    id SERIAL,
    user_id INTEGER NOT NULL,
    followee_id INTEGER NOT NULL,
    CONSTRAINT fw_users_fk
      FOREIGN KEY(user_id) 
	    REFERENCES users(user_id),
    CONSTRAINT fw_followees_fk
      FOREIGN KEY(followee_id)
	    REFERENCES users(user_id)
);

CREATE TABLE followers(
    id SERIAL,
    user_id INTEGER NOT NULL,
    follower_id INTEGER NOT NULL,
    CONSTRAINT fl_users_fk
      FOREIGN KEY(user_id) 
	    REFERENCES users(user_id),
    CONSTRAINT fl_followers_fk
      FOREIGN KEY(follower_id)
	    REFERENCES users(user_id)
);