from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm


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

# Custom Error Page - Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


# Custom Error Page - Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500
