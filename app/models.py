from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_code = db.Column(db.String(255))
    pitches = db.relationship('Pitch',backref = 'user', lazy = 'dynamic')

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_code = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.pass_code,password)    

    def __repr__(self):
        return f'User {self.username}'

class Pitch(db.Model):
    __tablename__='pitches'

    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String)
    pitch = db.Column(db.String)
    time = db.Column(db.DateTime,default=datetime.utcnow)  
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))      
    # Pitch.user.username