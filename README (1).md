# YOUR PROJECT TITLE
#### Video Demo: https://youtu.be/puO-Clw1BYk
#### Description: This is a program for managing tasks and chores. Going into this the plan was to make it easy and smooth to use. And the colors to be bright and positive everytime you looked at your chores.

# It's build using Python's Flask framework which provides an interactive web interface for users to create, update, and manage their own tasks.

# Using SQLAlchemy for mapping and data management with SQLite database. Im using SQLite for the database due to its simplicity and ease of setup. Flask's extensions are great to simplify common web development tasks, such as form handling, user authentication, and database operations.

# User registration and login functionality with Flasks' user authentication, Flask-Login. And password hashing with Flask-Bcrypt.

# 8 different app routes for: viewing tasks, creating new tasks, marking important tasks, updating existing tasks, and deleting tasks.

# Each route has a corresponding Html template.

# Using flash messaging to inform the user about feedback when performing operations.

# Option to "mark/unmark" tasks that are important, which are then displayed on the main page.

# Used WTForms to create form classes (Registration, Login, and Taskforms)



## App.py
# This is the main file that runs the web application. It sets up the Flask application, the database models, the user login manager, and all the application routes.

## create_db.py
# This Python script creates the SQLite database and tables for the project.

## requirements.txt
# This file lists all Python packages that the project depends on. You can install them with pip install -r requirements.txt.

## home.html, login.html, register.html, tasks.html, update_task.html
# These HTML files define the structure and layout of different web pages in the application. They're located in the templates folder and use Jinja2 templating syntax for dynamic content.

## layout.html
# This HTML file provides a base layout for all other HTML pages in the application. It includes the common elements such as the navigation bar and the flash message display.



### How to Run
# Install all dependencies using pip install -r requirements.txt.
# Run python create_db.py to set up the database.
# Start the Flask development server with python app.py.





## Degsign choices
# I appreciate the current design of the application, particularly the color scheme and its simplicity. However, to enhance the user experience, I would like to incorporate more dynamic features such as drag-and-drop functionality. I think thats better done with JavaScript and AJAX, but it was a little too advanced for me at this time. I went more heavy on the python back end. So, if I were to continue this project in the future, I would focus on enhancing my skills in JavaScript, AJAX, and advanced HTML techniques to create a more interactive and user-friendly interface.