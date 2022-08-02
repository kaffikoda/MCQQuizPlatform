from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flaskr.models import User, AdminDB, db
# from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_basicauth import BasicAuth
from flask_login import login_user, login_required, current_user, logout_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Database#2022@localhost/flask_movie'
app.config['SECRET_KEY'] = '12345'


def init_db():
    db.init_app(app)
    db.app = app
    db.create_all()


@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/login_page', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        entered_user_name = request.form.get("login_username")
        entered_password = request.form.get("login_password")

        user_data = User.query.filter_by(username=entered_user_name).first()

        if user_data is not None:
            if check_password_hash(user_data.hashed_password, entered_password):
                flash("Logged in", category="success")
            else:
                flash("Please enter correct password", category="error")
        else:
            flash("User doesn't exists")

    return render_template('login_page.html')


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
        admin_name_exists = AdminDB.query.filter_by(admin_username=user_name).first()
        admin_emailid_exists = AdminDB.query.filter_by(admin_emailid=user_emailid).first()

        if user_password != user_confirmed_password:
            print("Please type correct confirmed password")
            return redirect(url_for('signup_page'))
        elif user_name_exists is not None or user_emailid_exists is not None or admin_name_exists is not None or admin_emailid_exists is not None:
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



@app.route('/logout')
def logout():
    return render_template('homepage.html')


# @app.route('/admin')
# @basic_auth.required
# def admin():
#     return render_template('admin/index.html')


# admin = Admin(app)
# admin.add_view(ModelView(User, db.session))
# admin.add_view(ModelView(Admin, db.session))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)


# <a class="nav-link" href="/create-quiz">Create Quiz <span class="sr-only">(current)</span></a>