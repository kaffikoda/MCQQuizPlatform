from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user_test"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    user_emailid = db.Column(db.String(120), unique=True, nullable=False)
    user_first_name = db.Column(db.String(80), nullable=False)
    user_last_name = db.Column(db.String(80), nullable=False)
    user_created_at = db.Column(db.DateTime, nullable=False)
    hashed_password = db.Column(db.String(128), nullable=False)

    def __init__(self, username, user_emailid, user_first_name, user_last_name, user_created_at, hashed_password):
        self.username = username
        self.user_emailid = user_emailid
        self.user_first_name = user_first_name
        self.user_last_name = user_last_name
        self.user_created_at = user_created_at
        self.hashed_password = hashed_password

    def __repr__(self):
        return '<User %r>' % self.username
