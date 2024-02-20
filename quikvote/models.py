from datetime import datetime
from quikvote import db, login_manager
from flask_login import UserMixin

# Define the function to load a user by ID for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    """Load a user by ID for Flask-Login."""
    return User.query.get(int(user_id))

# Define the User model class
class User(db.Model, UserMixin):
    """User model class."""
    # Define columns for the User table
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    # Define a representation method for the User class
    def __repr__(self):
        """Representation of the User class."""
        return f"User('{self.username}', '{self.email}')"

# Define the Election model class
class Election(db.Model):
    """Election model class."""
    # Define columns for the Election table
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    voter_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Define relationships for the Election table
    candidates = db.relationship('Candidate', backref='election', lazy=True)
    votes = db.relationship('Vote', backref='election', lazy=True)

    # Define a representation method for the Election class
    def __repr__(self):
        """Representation of the Election class."""
        return f"Election('{self.title}', '{self.description}')"

# Define the Candidate model class
class Candidate(db.Model):
    """Candidate model class."""
    # Define columns for the Candidate table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    election_id = db.Column(db.Integer, db.ForeignKey('election.id'), nullable=False)

    # Define a relationship for the Candidate table
    votes = db.relationship('Vote', backref='candidate', lazy=True)

    # Define a representation method for the Candidate class
    def __repr__(self):
        """Representation of the Candidate class."""
        return f"Candidate('{self.name}', '{self.election.title}')"

# Define the Vote model class
class Vote(db.Model):
    """Vote model class."""
    # Define columns for the Vote table
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    election_id = db.Column(db.Integer, db.ForeignKey('election.id'), nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Define a representation method for the Vote class
    def __repr__(self):
        """Representation of the Vote class."""
        return f"Vote('{self.user.username}', '{self.election.title}', '{self.candidate.name}')"
