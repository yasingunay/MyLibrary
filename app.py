from cs50 import SQL
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import register_error, login_error, login_required, send_message

# Create the application instance
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///mylibrary.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Create a URL route in our application for "/"
@app.route('/', methods=['GET'])
def index():
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
        result = db.execute("INSERT INTO users(username, hash) VALUES(?,?)", username, password_hash)
    
        if result:
            # Log the user in
            user_data = db.execute("SELECT user_id FROM users WHERE username = ?", username)
            if user_data:
                user_id = user_data[0]["user_id"]
                session["user_id"] = user_id

                # Redirect to the index page
                return redirect("/")

        else:
            register_error("Registration failed!")
    

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
            user_id = rows[0]["user_id"]

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


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "GET":
        return render_template("add.html")
    else:
        category_name = request.form.get("category_name")
        if category_name == "":
            return send_message("Enter a category name!", "add.html")
        else:
            user_id = session.get("user_id")
            rows = db.execute("SELECT category_name FROM categories WHERE LOWER(category_name) = ? AND user_id = ?", category_name.lower(), user_id)
            if not rows:
                db.execute("INSERT INTO categories(user_id, category_name) VALUES (?, ?)",user_id, category_name)
                return send_message("Category successfully added!", "add.html")     
            else:
                return send_message("Category already exists!", "add.html")