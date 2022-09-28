from flask import render_template, request, redirect
from app import app
import users
import tweets

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not users.login(username, password):
            return render_template('login.html')
            
        return redirect('/home')

    return render_template('login.html')

@app.route('/logout')
def logout():
    return redirect('/')

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = 1

        if not users.signup(username, password, role):
            print('failing to sign up')
            return render_template('signup.html')
        
        return redirect('/home')
        
    return render_template('signup.html')

@app.route('/home')
def home():
    # users.require_role(1)
    # users.check_csrf()

    return render_template('home.html', tweets = tweets.get_tweets(users.user_id()))

@app.route('/tweet', methods = ['POST'])
def add_tweet():
    users.require_role(1)
    # users.check_csrf()

    user_id = users.user_id()

    if request.method == 'POST':
        post = request.form['post']

        tweets.add_tweet(post, user_id)

        return redirect('/home')

    return render_template('home.html')