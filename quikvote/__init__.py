import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = "de7a5386098e9f62a8a5245cfa535347"

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/quikvote'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + \
    os.environ.get('MYSQL_USER') + ':' + os.environ.get('MYSQL_PASSWORD') + \
    '@' + os.environ.get('MYSQL_HOST') + '/' + os.environ.get('MYSQL_DB')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
print(db.create_all)


from quikvote import routes
# with app.app_context():
#     db.create_all()
#     db.session.commit()

