from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Database#2022@localhost/flask_movie'
db = SQLAlchemy(app)


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


@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/signup_page', methods=["GET", "POST"])
def signup_page():
    if request.method == "POST":
        user_name = request.form.get("new_username")
        user_emailid = request.form.get("new_email")
        user_first_name = request.form.get("user_first_name")
        user_last_name = request.form.get("user_last_name")
        user_created_at = datetime.now()
        user_password = request.form.get("new_password")
        user_confirmed_password = request.form.get("new_confirm_password")

        hashed_password = generate_password_hash(user_password)

        user_name_exists = User.query.filter_by(username=user_name).first()
        user_emailid_exists = User.query.filter_by(user_emailid=user_emailid).first()

        if user_password != user_confirmed_password:
            print("Please type correct confirmed password")
            return redirect(url_for('signup_page'))
        elif user_name_exists is not None or user_emailid_exists is not None:
            print("User with the given credentials already exists")
            return redirect(url_for('homepage'))
        elif user_name_exists is None and user_emailid_exists is None:
            user_db_obj = User(user_name, user_emailid, user_first_name, user_last_name, user_created_at,
                               hashed_password)
            db.session.add(user_db_obj)
            db.session.commit()

        return render_template('homepage.html')
    else:
        return render_template('signup_page.html')


if __name__ == "__main__":
    app.run(debug=True)
