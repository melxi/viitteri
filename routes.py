from flask import render_template, request, redirect, session, json
from flask_cors import cross_origin
from app import app
import users
import tweets
import replies

@app.route('/')
def index():
    if session.get('logged_in') is True:
        return redirect('/home')

    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not users.login(username, password):
            return render_template('login.html')
        return redirect('/home')

    if session.get('logged_in') is True:
        return redirect('/home')
    return render_template('login.html')

@app.route('/logout')
def logout():
    users.logout()
    return redirect('/')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not users.signup(username, password):
            return render_template('signup.html')
        return redirect('/home')
    return render_template('signup.html')

@app.route('/home')
def home():
    if not users.require_role(1):
        return redirect('/')
    return render_template('home.html', tweets = tweets.get_tweets(users.user_id()), users = users.get_users())

@app.route('/follow', methods=['POST'])
@cross_origin()
def follow():
    users.require_role(1)

    user_id = users.user_id()

    if request.method == 'POST':
        data = request.get_json()
        followee_id = data

        users.follow_user(user_id, followee_id)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/tweet', methods = ['POST'])
def add_tweet():
    users.require_role(1)
    users.check_csrf()

    user_id = users.user_id()

    if request.method == 'POST':
        post = request.form['post']

        tweets.add_tweet(post, user_id)
        return redirect('/home')
    return render_template('home.html')

@app.route('/tweet/<int:tweet_id>', methods = ['GET'])
def get_tweet(tweet_id):
    return render_template('tweet.html', tweet=tweets.get_tweet(tweet_id), replies=replies.get_replies(tweet_id))

@app.route('/<string:username>', methods=['GET'])
def get_profile(username):
    return render_template('profile.html', user = users.get_user(), users = users.get_users(), tweets = tweets.get_tweets(users.user_id()),)

@app.route('/<string:username>/following', methods=['GET'])
def get_followees(username):
    users.require_role(1)
    return render_template('following.html', user = users.get_user(), followees = users.get_followees())

@app.route('/<string:username>/followers', methods=['GET'])
def get_followers(username):
    users.require_role(1)
    return render_template('followers.html', user = users.get_user(), followers = users.get_followers())

@app.route('/reply', methods= ['POST'])
def add_reply():
    users.require_role(1)
    users.check_csrf()

    user_id = users.user_id()

    if request.method == 'POST':
        post = request.form['post']
        tweet_id = request.form['tweet_id']

        replies.add_reply(tweet_id, user_id, post)
        return redirect(request.referrer)
    return render_template('home.html')
