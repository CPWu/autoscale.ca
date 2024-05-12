from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm, NameForm, UserForm, PasswordForm, PostForm
from app.models import User, Post
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date

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

# User Add
@app.route("/user/add", methods=["GET", "POST"])
def add_user():
    name = None
    form = UserForm()
    # Validate Form
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            # Hash Password
            hashed_password = generate_password_hash(form.password_hash.data)
            user = User(name=form.name.data, email=form.email.data, favourite_color=form.favourite_color.data, password_hash=hashed_password) 
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.favourite_color = ''
        form.password_hash = ''
        flash("User Added Successfully")
    our_users = User.query.order_by(User.date_added)
    return render_template("add_user.html", form=form, name=name, our_users=our_users)

# Update Database Record
@app.route("/update/<int:id>", methods=["GET","POST"])
def update(id):
    form = UserForm()
    name_to_update = User.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favourite_color = request.form['favourite_color']
        try:
            db.session.commit()
            flash("User Updated Succesfuly")
            return render_template("update.html", form=form, name_to_update=name_to_update)     
        except:
            flash("Error! Problem occurred... try again..")
            return render_template("update.html", form=form, name_to_update=name_to_update) 
    else:
        return render_template("update.html", form=form, name_to_update=name_to_update, id=id) 

# User Deletion
@app.route("/delete/<int:id>")
def delete(id):
    user_to_delete = User.query.get_or_404(id)   
    name = None
    form = UserForm()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Successfully")
        our_users = User.query.order_by(User.date_added)
        return render_template("add_user.html", form=form, name=name, our_users=our_users)
    except:       
        flash("Error occurred during user deletion.")  
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

# Create Password Test Page
@app.route("/test_pw", methods=['GET','POST'])
def test_pw(): 
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()
    # Validate Form
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        # Clear the form
        form.email.data = ''
        form.password_hash.data = ''

        pw_to_check = User.query.filter_by(email=email).first()
        
        # Check Hashed Password
        passed = check_password_hash(pw_to_check.password_hash, password)

    return render_template('test_pw.html', email=email, password=password, pw_to_check=pw_to_check, passed=passed, form=form)

@app.route("/add-post", methods=["GET", "POST"])
def add_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=form.author.data, slug=form.slug.data)
        # Clear Form
        form.title.data = ''
        form.content.data = ''
        form.author.data = ''
        form.slug.data = ''

        # Add to DB
        db.session.add(post)
        db.session.commit()

        # Flash Message
        flash("Post Submitted Successfully!")

        # Redirect
    return render_template("add_post.html", form=form)
 
@app.route("/posts", methods=["GET"])
def posts():
    # Get All Posts from DB
    posts = Post.query.order_by(Post.date_posted)

    return render_template("posts.html", posts=posts)

@app.route("/posts/<int:id>")
def post(id):
    post = Post.query.get_or_404(id)
    return render_template("post.html", post=post)

@app.route("/posts/edit/<int:id>", methods=["GET","POST"])
def edit_post(id):
    post = Post.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data
        # Commit
        db.session.add(post)
        db.session.commit()
        flash("Post has been updated!")
        return redirect(url_for('post',id=post.id))
    form.title.data = post.title
    form.author.data = post.author
    form.slug.data = post.slug
    form.content.data = post.content
    return render_template('edit_post.html',form=form)

@app.route("/posts/delete/<int:id>")
def delete_post(id):
    post_to_delete = Post.query.get_or_404(id)
    try:
        db.session.delete(post_to_delete)
        db.session.commit()

        # Return Message
        flash("Post was successfully deleted!")
        
        # Get All Posts from DB
        posts = Post.query.order_by(Post.date_posted)
        return render_template("posts.html", posts=posts)
    except:
        flash("Error deleting post, try again")
        # Get All Posts from DB
        posts = Post.query.order_by(Post.date_posted)
        return render_template("posts.html", posts=posts) 

# Custom Error Page - Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Custom Error Page - Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500
