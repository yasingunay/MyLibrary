# MyLibrary - CS50 Final Project
#### Video Demo:  <https://youtu.be/nNyIe7emT2M>

Welcome to the MyLibrary as a Library Management System! This web application is designed to help you organize and manage your personal library of items. Whether it's books, movies, or any other items you want to keep track of, this application has you covered. Let's take a detailed look at what this project is all about and how it works.

## Project Overview
MyLibrary is a Flask-based web application that provides users with the ability to register, log in, organize items into categories, and perform various library management tasks. It is built using Flask, SQL, and other related libraries. The main functionalities include:

* User registration and authentication
* Adding, viewing, and deleting categories
* Adding, viewing, and deleting items within categories
* Changing user passwords


## Files and Their Functions
Here's an overview of the main files in the project and their functions:

* app.py: This is the heart of the application, containing all the Flask routes and functions that handle different user actions. It's responsible for rendering templates, interacting with the database, and implementing user authentication.

* helpers.py: This file contains helper functions that are used throughout the application. It includes the login_required decorator, which ensures that only authenticated users can access certain routes, as well as functions like send_message and validate_password.

* templates folder: This directory contains all the HTML templates used to render different pages of the application. Each template corresponds to a specific functionality, such as registration, login, adding categories, adding items, and more.


## Design Choices
When designing the MyLibrary, mostly I've used CS50 Finance design. 

* Security: Security is a top priority. Passwords are securely stored in the database using hashed versions, which helps protect user data even if the database is compromised.

* User Experience: The application provides clear and user-friendly interfaces for different tasks, guiding users through each step. Flash messages are used to provide immediate feedback to users.

* Database Structure: The SQLite database is structured to store user information, categories, and items. This design allows for efficient retrieval of data when rendering different pages.

* Password Change: Users can change their passwords using the "Change Password" functionality. The old password is verified against the hashed version in the database, and new passwords are securely hashed before being stored.

* Session Management: Flask's session management is utilized to keep track of user sessions and maintain their login status. This ensures that users don't have to log in repeatedly during their session.

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

## Conclusion
MyLibrary is a comprehensive Flask web application designed to help users organize and manage their personal libraries. Its user-friendly interface, secure authentication, and efficient database design make it a valuable tool for anyone looking to keep track of their items. Whether you're managing a collection of books, movies, or anything else, this application is here to assist you. Enjoy using it and feel free to contribute to its improvement!

![50!](https://miro.medium.com/v2/resize:fit:1400/1*eD8btFfojRagaSs7awJsaA.png)
