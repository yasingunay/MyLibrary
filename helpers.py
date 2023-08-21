from flask import redirect, render_template, session
from functools import wraps



def register_error(message):
    return render_template("register.html", message = message)

def login_error(message):
    return render_template("login.html", message = message)

def send_message(message, page):
    return render_template(page, message = message)


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