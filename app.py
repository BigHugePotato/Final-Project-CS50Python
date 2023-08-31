from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, current_user, login_required, logout_user
from flask_wtf import FlaskForm
from flask_bcrypt import Bcrypt
from datetime import datetime
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


app = Flask(__name__)
app.config["SECRET_KEY"] = "123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    #email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    tasks = db.relationship("Task", backref="author", lazy=True)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    is_marked = db.Column(db.Boolean, default=False)


class TaskForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=100)])
    content = StringField("Content", validators=[DataRequired()])
    submit = StringField("Create Task")


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(),  Length(min=2, max=20)])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You can now log in you handsome boy", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check username and password", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/task/<int:task_id>/update", methods=["GET", "POST"])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.author != current_user:
        abort(403)
    form = TaskForm()
    if form.validate_on_submit():
        task.title = form.title.data
        task.content = form.content.data
        db.session.commit()
        flash("Your task has been updated!", "success")
        return redirect(url_for("tasks"))
    elif request.method == "GET":
        form.title.data = task.title
        form.content.data = task.content
    return render_template("update_task.html", title="Update Task", form=form)


@app.route("/task/<int:task_id>/delete", methods=["GET"])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.author != current_user:
        abort(403)
    db.session.delete(task)
    db.session.commit()
    flash("Your task has been deleted!", "success")
    return redirect(url_for("tasks"))


#Home page
@app.route("/",  methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(title=form.title.data, content=form.content.data, date_posted=datetime.utcnow(), author=current_user)
        db.session.add(task)
        db.session.commit()
        flash("Task created successfully!", "success")
        return redirect(url_for("home"))

    tasks = Task.query.filter_by(user_id=current_user.id, is_marked=True).all()
    return render_template("home.html", important_tasks=tasks)


@app.route("/tasks",  methods=["GET", "POST"])
@login_required
def tasks():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(title=form.title.data, content=form.content.data, user_id=current_user.id, date_posted=datetime.utcnow())
        db.session.add(task)
        db.session.commit()
        flash("Your task has been created!", "success")
        return redirect(url_for("tasks"))

    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template("tasks.html", title="Your Tasks", form=form, tasks=tasks)


@app.route("/task/<int:task_id>/mark", methods=["GET", "POST"])
@login_required
def mark_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.author != current_user:
        abort(403)
    if task.is_marked:
        task.is_marked = False
        db.session.commit()
        flash("Unmarked", "success")
    else:
        task.is_marked = True
        db.session.commit()
        flash("Marked", "success")
    return redirect(url_for("tasks"))


if __name__ == "__main__":
    app.run(debug=True)