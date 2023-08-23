# MyLibrary
CS50 Final Project


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