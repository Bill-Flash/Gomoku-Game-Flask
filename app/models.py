from datetime import datetime
from app import db


class User(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(40), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    win = db.Column(db.INTEGER, default=0)
    lose = db.Column(db.INTEGER, default=0)
    draw = db.Column(db.INTEGER, default=0)
    rate = db.Column(db.REAL, default=0)
    records = db.relationship('Competition', backref='participant', lazy='dynamic')
    profile = db.relationship('Profile', backref='user',lazy='dynamic')
    avatar = db.relationship('Avatar', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Competition(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'), primary_key=True)
    result = db.Column(db.String(20), index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return 'The competition {}: Participant: {} Result: {} At Time: {}'\
            .format(self.id,self.user_id, self.result, self.timestamp)


class Profile(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    gender = db.Column(db.String(15), index=True)
    intro = db.Column(db.String(50), index=True)
    profile_photo = db.Column(db.String(256))
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Profile for player: {}, gender: {}, introduction: {}>'\
            .format(self.user_id,self.gender, self.intro)

class Avatar(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    avatar = db.Column(db.String(256))
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Avatar for player: {} in {}>'\
            .format(self.user_id, self.avatar)