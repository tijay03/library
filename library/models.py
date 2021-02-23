from library import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    usertype = db.Column(db.String(20), nullable=False)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Book(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def  __repr__(self):
        return f"Book('{self.genre}', '{self.title}')"
