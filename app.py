from cs50 import SQL
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import error

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

        existing_user = db.execute("SELECT username FROM users WHERE username = ?", username)

        if username == "" or existing_user:
            return error("Username is not avaiable!")
        elif password == "":
            return error("Missing password!")
        elif confirmation == "" or (password != confirmation):
            return error("Passwords don't match!")
        

        # Generate a hasf of the password
        password_hash = generate_password_hash(
            password, method="pbkdf2", salt_length=16
        )

        # Add user to database
        db.execute("INSERT INTO users(username, hash) VALUES(?,?)", username, password_hash)

        return redirect("/")