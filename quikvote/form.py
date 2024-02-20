# Importing necessary modules
from collections.abc import Mapping, Sequence  # For abstract base classes
from flask_login import current_user  # For accessing the current user
from flask_wtf import FlaskForm  # For creating Flask forms
from wtforms import StringField, PasswordField, SubmitField, BooleanField  # For form fields
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError  # For form validation
from quikvote.models import User  # For accessing the User model from quikvote package

# Creating a registration form class inheriting from FlaskForm
class RegistrationForm(FlaskForm):
    """Form for user registration."""
    
    def __init__(self, *args, **kwargs):
        """Initialize the registration form."""
        super().__init__(*args, **kwargs)

    # Form fields with validators and placeholders
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)], render_kw={"placeholder": "Enter your username"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Enter your email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Enter your password"})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Confirm your password"})
    submit = SubmitField('Sign up')

    # Custom validation for username uniqueness
    def validate_username(self, username):
        """Validate uniqueness of username."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken')
        
    # Custom validation for email uniqueness
    def validate_email(self, email):
        """Validate uniqueness of email."""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken')

# Creating a login form class inheriting from FlaskForm
class LoginForm(FlaskForm):
    """Form for user login."""
    
    def __init__(self, *args, **kwargs):
        """Initialize the login form."""
        super().__init__(*args, **kwargs)

    # Form fields with validators and placeholders
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Enter your email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Enter your password"})
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login') 

# Creating an update account form class inheriting from FlaskForm
class UpdateAccountForm(FlaskForm):
    """Form for updating user account information."""
    
    def __init__(self, *args, **kwargs):
        """Initialize the update account form."""
        super().__init__(*args, **kwargs)

    # Form fields with validators and placeholders
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)], render_kw={"placeholder": "Change your username"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Change your email"})
    submit = SubmitField('Update')

    # Custom validation for username uniqueness
    def validate_username(self, username):
        """Validate uniqueness of username."""
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken')
            
    # Custom validation for email uniqueness
    def validate_email(self, email):
        """Validate uniqueness of email."""
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken')
