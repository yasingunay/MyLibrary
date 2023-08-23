# MyLibrary - CS50 Final Project
#### Video Demo:  <https://youtu.be/nNyIe7emT2M>

## Description:
This is a Flask web application that serves as a simple personal library management system. The application is structured to manage a user's personal library inventory.
It allows users to 
* register
* log in, log out
* add categories for organizing items
* add items to those categories 
* view items and categories 
* delete items and categories 
* change their password

This web app contains separate routes for different functionalities and contains separate HTML templates. I've also included user authentication and authorization mechanisms with hashed passwords and session management, which is essential for security. Additionally, I'm using SQLite as the database to store user information, categories, and items. I have also provided meaningful flash messages to users for feedback. In terms of design choice, I've used CS50 Finance design.



## Requirements 
* Flask
* Flask-Session
* cs50





## Useful Sources
* [The Built-In Debugger](https://flask.palletsprojects.com/en/2.3.x/debugging/)
* [Bootstrap - Buttons](https://getbootstrap.com/docs/4.0/components/buttons/)
* [Favicon Generators](https://favicon.io/)

## Tips
* Use flask in debuggin mod (flask --app app run --debug)


