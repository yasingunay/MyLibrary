from flask import render_template


def register_error(message):
    return render_template("register.html", message = message)

def login_error(message):
    return render_template("login.html", message = message)