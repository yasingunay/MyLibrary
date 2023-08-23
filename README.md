# MyLibrary - CS50 Final Project
#### Video Demo:  <https://youtu.be/nNyIe7emT2M>
#### Description:
This is a Flask web application that serves as a simple personal library management system. 
It allows users to 
* register
* log in, log out
* add categories for organizing items
* add items to those categories 
* view items and categories 
* delete items and categories 
* change their password

The application is structured to manage a user's personal library inventory.

## Requirements 
* Flask
* Flask-Session
* cs50

## Useful Sources
* [The Built-In Debugger](https://flask.palletsprojects.com/en/2.3.x/debugging/)
* [Bootstrap - Buttons](https://getbootstrap.com/docs/4.0/components/buttons/)
* [Favicon Generators](https://favicon.io/)

# Tips
Use flask in debuggin mod (flask --app app run --debug)


# Database Structure
CREATE TABLE users(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL
)

CREATE TABLE categories (
user_id INTEGER NOT NULL,
    category_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    category_name VARCHAR(255) NOT NULL,
FOREIGN KEY (user_id) REFERENCES users(user_id)
)

CREATE TABLE items (
user_id INTEGER NOT NULL,
    item_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    category_id INT,
    item_name VARCHAR(255) NOT NULL,
    item_note TEXT,
FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
 )
