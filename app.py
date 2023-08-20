from cs50 import SQL
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import register_error, login_error

# Create the application instance
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

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

        # Check errors
        if username == "" or existing_user:
            return register_error("Username is not avaiable!")
        elif password == "":
            return register_error("Missing password!")
        elif confirmation == "" or (password != confirmation):
            return register_error("Passwords don't match!")
        

        # Generate a hasf of the password
        password_hash = generate_password_hash(
            password, method="pbkdf2", salt_length=16
        )

        # Add user to database
        db.execute("INSERT INTO users(username, hash) VALUES(?,?)", username, password_hash)

        return redirect("/")
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Forget any user_id
    session.clear()
    
    # Get username and password via form
    username = request.form.get("username")
    password = request.form.get("password")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not username:
            return login_error("Please enter a username")
        # Ensure password was submitted
        elif not password:
            return login_error("Please enter a password")
        
        # Query database for user
        rows = db.execute("SELECT * FROM users WHERE username is ?", username)
        if len(rows) == 1:
            password_hash = rows[0]["hash"]
            user_id = rows[0]["id"]

        elif len(rows) != 1 or not check_password_hash(password_hash,password):
            return login_error("Invalid username and/or password")
        
        # Remember which user has logged in
        session["user_id"] = user_id

         # Redirect user to home page
        return redirect("/")
    
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    

@app.route("/logout", methods=["GET", "POST"])
def logout():
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")