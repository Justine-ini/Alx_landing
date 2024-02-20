# Importing necessary modules
from flask import render_template, url_for, flash, redirect, request  # For Flask web framework functionality
from quikvote.models import User  # Importing the User model
from quikvote.forms import RegistrationForm, LoginForm, UpdateAccountForm  # Importing the forms for user registration, login, and account update
from quikvote import app, db, bcrypt  # Importing the Flask app instance, database instance, and bcrypt for password hashing
from flask_login import login_user, logout_user, current_user, login_required  # For user session management

# Route for the home page
@app.route("/", methods=["GET", "POST"])
def home():
    """Render the home page."""
    return render_template("index.html", title="home")

# Route for user login
@app.route("/login", methods=["GET", "POST"])
def login():
    """Render the login page and handle user login."""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Login Unsuccessful. Check email and password.", "danger")
    return render_template("login.html", title="Login", form=form)

# Route for user registration
@app.route("/register", methods=["GET", "POST"])
def register():
    """Render the registration page and handle user registration."""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        try:
            db.session.add(user)
            db.session.commit()
            flash(f"Account created for {form.username.data}!", "success")
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash("An error occurred. Please try again.", "danger")
    return render_template("register.html", title="Register", form=form)

# Route for user logout
@app.route("/logout")
def logout():
    """Handle user logout."""
    logout_user()
    return redirect(url_for('home'))

# Route for user account management
@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    """Render the account page and handle account updates."""
    form = UpdateAccountForm()
    if form.validate_on_submit():
        try:
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Your account has been updated!', 'success')
            return redirect(url_for('account'))
        except Exception as e:
            db.session.rollback()
            flash("An error occurred. Please try again.", "danger")
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)

# Route to create a new election
@app.route("/create_election", methods=["GET", "POST"])
def create_election():
    """Render the page to create a new election."""
    return render_template("create_election.html")
