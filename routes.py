from flask import render_template, request, redirect
from app import app
import users

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if (request.method == 'POST'):
        print('login request')
        username = request.form['username']
        password = request.form['password']
        print(username)
        print(password)

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

        if not users.signup(username, password):
            return render_template('signup.html')
        
        return redirect('/home')
        
    return render_template('signup.html')

@app.route('/home')
def home():
    return render_template('home.html')