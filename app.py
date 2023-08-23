from cs50 import SQL
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, send_message


# Create the application instance
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///mylibrary.db")

# Ensure templates are auto-reloaded
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Create a URL route in our application for "/"
@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    user_id = session.get("user_id")
    if request.method == "POST":
        # Get the category name from the form
        category_name = request.form.get("category_name")
        rows = db.execute("SELECT category_id FROM categories WHERE category_name = ?", category_name)
        category_id = rows[0]["category_id"]

        # Query database for items and categories in the selected category
        items = db.execute("SELECT item_name, item_note FROM items WHERE user_id = ? AND category_id = ?", user_id, category_id )
        categories = db.execute("SELECT category_name FROM categories WHERE user_id = ?", user_id)
        if not items:
                flash("Your category is empty!")
        return render_template('index.html', items = items, categories = categories)
    else:
        # Query database for items and categories
        items = db.execute("SELECT item_name, item_note FROM items WHERE user_id = ?", user_id )
        categories = db.execute("SELECT category_name FROM categories WHERE user_id = ?", user_id)

        # Check if there are any items if not show a message
        if not items:
                flash("No items!")
        # Render the index.html template with the items and categories
        return render_template('index.html', items = items, categories = categories)
       

# Create a URL route in our application for "/register"
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template('register.html')
    else:
        # Get data from register from
        username = request.form.get("username").lower() # Convert username to lowercase
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check if username is already taken
        existing_user = db.execute("SELECT username FROM users WHERE LOWER (username) = ?", username) # Convert username to lowercase

        # Check if username, password and confirmation are valid
        if not username or existing_user:
            return send_message("Username is not avaiable!", "register.html")
        elif not password:
            return send_message("Missing password!", "register.html")
        elif not confirmation or password != confirmation:
            return send_message("Passwords don't match!", "register.html")
        else:
            # Generate a hasf of the password
            password_hash = generate_password_hash(
                password, method="pbkdf2", salt_length=16
            )

            # Add user to database
            result = db.execute("INSERT INTO users(username, hash) VALUES(?,?)", username, password_hash)
        
            # Check if the user was added to the database
            if result:
                # Log the user in
                user_data = db.execute("SELECT user_id FROM users WHERE username = ?", username)
                if user_data:
                    user_id = user_data[0]["user_id"]
                    session["user_id"] = user_id
                    return redirect("/")
                else:
                    return send_message("Error logging in!", "register.html")
            else:
                return send_message("Error registering user!", "register.html")
            
        
    

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
            return send_message("Please enter a username", "login.html")
        
        # Ensure password was submitted
        elif not password:
            return send_message("Please enter a password", "login.html")
            
        # Query database for user
        rows = db.execute("SELECT * FROM users WHERE username is ?", username)
        if len(rows) == 1:
            password_hash = rows[0]["hash"]
            user_id = rows[0]["user_id"]

        elif len(rows) != 1 or not check_password_hash(password_hash,password):
            return send_message("Invalid username and/or password", "login.html")
            
        
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


@app.route("/add_category", methods=["GET", "POST"])
@login_required
def add_category():
    if request.method == "GET":
        return render_template("add_category.html")
    else:
        category_name = request.form.get("category_name")
        # Check if category name is valid
        if category_name == "":
            return send_message("Enter a category name!", "add_category.html")
        else:
            # Check if category already exists
            user_id = session.get("user_id")
            rows = db.execute("SELECT category_name FROM categories WHERE LOWER(category_name) = ? AND user_id = ?", category_name.lower(), user_id)
            if not rows:
                db.execute("INSERT INTO categories(user_id, category_name) VALUES (?, ?)",user_id, category_name.capitalize())
                flash("Category successfully added!")     
                return redirect("/categories")
            else:
                # If category already exists show a message
                return send_message("Category already exists!", "add_category.html")
            



@app.route("/add_item", methods=["GET", "POST"])
@login_required
def add_item():
    user_id = session.get("user_id")
    if request.method == "GET":
        # Query database for categories
        categories = db.execute("SELECT category_name FROM categories WHERE user_id = ? ", user_id)
        return render_template("add_item.html", categories = categories)
    else:
        # Get data from form
        item_name = request.form.get("item_name")
        item_note = request.form.get("item_note")
        category_name = request.form.get("category_name")

        # Query database for category_id
        rows = db.execute("SELECT category_id FROM categories WHERE category_name = ? AND user_id = ?", category_name, user_id)
        category_id = rows[0]["category_id"]

        # Add item to database
        db.execute("INSERT INTO items(item_name, item_note, category_id, user_id) VALUES (?, ?, ?, ?)", item_name, item_note, category_id, user_id)

        # Show a message if item was added
        flash("Item successfully added!")

        # Redirect to the index page
        return redirect(url_for("index")) 
    

@app.route("/delete_item", methods=["GET", "POST"])
@login_required
def delete_item():
    if request.method == "POST":
        user_id = session.get("user_id")
        rows = db.execute("SELECT item_id, item_name, item_note FROM items WHERE user_id = ?", user_id)
        item_id = request.form.get("item_id")
        db.execute("DELETE FROM items WHERE user_id = ? AND item_id = ?", user_id, item_id)
        flash("Item deleted!")
        return redirect("/delete_item")
    else:
        # Query database for items
        user_id = session.get("user_id")
        rows = db.execute("SELECT item_id, item_name, item_note FROM items WHERE user_id = ?", user_id)

        # Check if there are any items
        if not rows:
            return redirect("/")
        
        # Render the delete_item.html template with the items
        return render_template("delete_item.html" ,rows = rows)

    


@app.route("/categories", methods = ["GET", "POST"])
@login_required
def categories():
    user_id = session.get("user_id")
    if request.method == "GET":
        # Query database for categories
        rows = db.execute("SELECT category_name FROM categories WHERE user_id = ?", user_id)
        if not rows:
            flash("You have no categories!")
        return render_template("categories.html", rows = rows)
    

@app.route("/delete_category", methods = ["GET", "POST"])
@login_required
def delete_category():
    user_id = session.get("user_id")
    # Query database for categories
    rows = db.execute("SELECT category_name, category_id FROM categories WHERE user_id = ?", user_id)
    if request.method == "GET":
        # Check if there are any categories if not show a message
        if len(rows) == 0:
             flash("There are no categories that can be deleted!")
        return render_template("delete_category.html", rows = rows)
    else: 
        category_id= request.form.get("category_id")

        # Check if category contains items
        items_in_category = db.execute("SELECT COUNT(*) FROM items WHERE user_id = ? AND category_id = ?", user_id, category_id)
        num_items = items_in_category[0]["COUNT(*)"]

        # Delete category if it doesn't contain any items
        if num_items > 0:
            flash("Cannot delete the category. It contains items.")
        else:
            db.execute("DELETE FROM categories WHERE user_id = ? AND category_id = ?", user_id, category_id)
            flash("Category deleted!")
        return redirect("/delete_category")
        
