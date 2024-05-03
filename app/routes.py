from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm, NameForm, UserForm
from app.models import User
from app import db

@app.route("/")
@app.route("/index")
def index():
    user = {"username": "Everyone"}
    return render_template("index.html", title="Home", user=user)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(
            "Login requested for user {}, remember_me={}".format(
                form.username.data, form.remember_me.data
            )
        )
        return redirect(url_for("index"))
    return render_template("login.html", title="Sign In", form=form)

# User Profile Page
@app.route("/user/<name>")
def user(name): 
    return render_template('user.html', user_name=name)

@app.route("/user/add", methods=["GET", "POST"])
def add_user():
    name = None
    form = UserForm()
    # Validate Form
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            user = User(name=form.name.data, email=form.email.data) 
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash("User Added Successfully")
    our_users = User.query.order_by(User.date_added)
    return render_template("add_user.html", form=form, name=name, our_users=our_users)

# Create Name Page
@app.route("/name", methods=['GET','POST'])
def name(): 
    name = None
    form = NameForm()
    # Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash('Form Submitted Successfully')
    return render_template('name.html', name=name, form=form)

# Custom Error Page - Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Custom Error Page - Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500
