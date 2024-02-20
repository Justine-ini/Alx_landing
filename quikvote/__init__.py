# Importing necessary modules
import os  # For accessing environment variables
from flask import Flask  # For creating Flask application
from flask_sqlalchemy import SQLAlchemy  # For handling database operations
from flask_bcrypt import Bcrypt  # For encrypting passwords
from flask_login import LoginManager  # For managing user sessions

# Creating a Flask application instance
app = Flask(__name__)

# Setting a secret key for the application
app.config["SECRET_KEY"] = "de7a5386098e9f62a8a5245cfa535347"

# Configuring the SQLAlchemy database URI
# The database URI is retrieved from environment variables for security reasons
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + \
    os.environ.get('MYSQL_USER') + ':' + os.environ.get('MYSQL_PASSWORD') + \
    '@' + os.environ.get('MYSQL_HOST') + '/' + os.environ.get('MYSQL_DB')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Creating an instance of the SQLAlchemy class, passing the app object
db = SQLAlchemy(app)

# Creating an instance of the Bcrypt class, passing the app object
bcrypt = Bcrypt(app)

# Creating an instance of the LoginManager class, passing the app object
login_manager = LoginManager(app)

# Configuring the login view for the LoginManager
login_manager.login_view = 'login'

# Importing routes module from the quikvote package
from quikvote import routes

# Uncomment the following lines if you want to create database tables automatically
# with app.app_context():
#     db.create_all()
#     db.session.commit()
