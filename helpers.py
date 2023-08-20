from flask import render_template


def error(message):
    return render_template("register.html", message = message)