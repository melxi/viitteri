from os import getenv
from flask import Flask

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

if __name__ == '__main__':
    app.run(debug=True)
