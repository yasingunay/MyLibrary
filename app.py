from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

# Create the application instance
app = Flask(__name__)



# Create a URL route in our application for "/"
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == "GET":
        return render_template('layout.html')
    

