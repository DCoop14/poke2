from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


squad5 = db.Table('my5',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('pokemon_id', db.Integer, db.ForeignKey('pokemon.id')),
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True) 
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    team = db.relationship(
        'Pokemon',
        secondary = squad5,
        backref= 'users',        
        lazy='dynamic'
    )

    def __init__(self, username, first_name, last_name,  email, password):
            self.username = username
            self.first_name = first_name
            self.last_name = last_name
            self.email = email
            self.password = generate_password_hash(password)


class Team(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    win_id = db.Column(db.Integer, db.ForeignKey('win_id'))

    def __init__(self, id, user_id, win_id):
        self.id = id
        self.user_id = user_id
        self.win_id = win_id

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poke_img = db.Column(db.String(300))
    name = db.Column(db.String(50), unique = True)
    ability = db.Column(db.String(50))
    hp_stat = db.Column(db.Integer)
    atk_stat = db.Column(db.Integer)
    def_stat = db.Column(db.Integer)
    

    def __init__(self, poke_img, name, ability, hp_stat, atk_stat, def_stat):
        self.poke_img = poke_img
        self.name = name
        self.ability = ability
        self.hp_stat = hp_stat
        self.atk_stat = atk_stat
        self.def_stat = def_stat

