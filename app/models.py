from . import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    pitches = db.relationship('Pitch',backref = 'user', lazy = 'dynamic')

    def __repr__(self):
        return f'User {self.username}'

class Pitch(db.Model):
    __tablename__='pitches'

    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String)
    pitch = db.Column(db.String) 
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))              

    # Pitch.user.username