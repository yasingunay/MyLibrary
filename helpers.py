from flask import redirect, render_template, session
from functools import wraps

# Function to send message to user
def send_message(message, page):

    return render_template(page, message = message)


# Function to check if user is logged in
def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function