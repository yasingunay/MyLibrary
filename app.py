from cs50 import SQL
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

# Create the application instance
app = Flask(__name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///mylibrary.db")


# Create a URL route in our application for "/"
@app.route('/', methods=['GET'])
def hello_world():
    if request.method == "GET":
        return render_template('index.html')
    

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template('register.html')
    else:
        # Get data from register from
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

