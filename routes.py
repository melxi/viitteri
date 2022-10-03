from flask import render_template, request, redirect, session, json
from app import app
import users
import tweets

@app.route('/')
def index():
    print(session.get('logged_in'))
    if session.get('logged_in') == True:
        return redirect('/home')

    return render_template('index.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not users.login(username, password):
            return render_template('login.html')
            
        return redirect('/home')

    if session.get('logged_in') == True:
        return redirect('/home')

    return render_template('login.html')

@app.route('/logout')
def logout():
    users.logout()
    return redirect('/')

@app.route('/signup', methods = ['GET', 'POST'])
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
def follow():
    users.require_role(1)

    user_id = users.user_id()

    if request.method == 'POST':
        data = request.get_json()
        print(data)
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
    
    return render_template('tweet.html', tweet=tweets.get_tweet(tweet_id))

@app.route('/<string:username>', methods=['GET'])
def get_profile(username):
    
    return render_template('profile.html', user = users.get_user(), users = users.get_users(), tweets = tweets.get_tweets(users.user_id()),)