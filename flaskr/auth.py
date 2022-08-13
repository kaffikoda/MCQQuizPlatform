from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flaskr.models import db, User, AdminDB, QuestionSetter
from datetime import datetime
from flask_login import login_user, login_required, current_user, logout_user

auth = Blueprint("auth", __name__)


@auth.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        entered_user_name = request.form.get("loginUserName")
        entered_password = request.form.get("loginPassword")

        user_data = User.query.filter_by(username=entered_user_name).first()
        admin_data = AdminDB.query.filter_by(admin_username=entered_user_name).first()
        question_setter_data = QuestionSetter.query.filter_by(question_setter_username=entered_user_name).first()

        # print(isinstance(user_data, User))
        # print(isinstance(admin_data, AdminDB))
        # print(isinstance(question_setter_data, QuestionSetter))
        #
        # print(user_data)
        # print(admin_data)
        # print(question_setter_data)

        if user_data is not None:
            if check_password_hash(user_data.hashed_password, entered_password):
                login_user(user=user_data, remember=True)
                # flash(f"Welcome back, {current_user.username}!!!!!", category="success")
                return redirect(url_for('views.home'))
            else:
                flash("Please enter correct password", category="warning")
        elif admin_data is not None:
            if check_password_hash(admin_data.hashed_password, entered_password):
                login_user(user=admin_data, remember=True)
                # flash(f"Welcome back, {current_user.admin_username}!!!!!", category="success")
                return redirect(url_for('views.home'))
            else:
                flash("Please enter correct password", category="warning")
        elif question_setter_data is not None:
            if check_password_hash(question_setter_data.hashed_password, entered_password):
                login_user(user=question_setter_data, remember=True)
                # flash(f"Welcome back, {current_user.question_setter_username}!!!!!", category="success")
                return redirect(url_for('views.home'))
            else:
                flash("Please enter correct password", category="warning")
        else:
            flash("Entered username doesn't exists", category="info")

    return render_template('login_page.html')


@auth.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        user_name = request.form.get("inputUserName")
        user_emailid = request.form.get("inputEmail")
        user_first_name = request.form.get("inputFirstName")
        user_last_name = request.form.get("inputLastName")
        user_created_at = datetime.now()
        user_password = request.form.get("inputPassword")
        user_confirmed_password = request.form.get("inputConfirmPassword")

        hashed_password = generate_password_hash(user_password)

        user_name_exists = User.query.filter_by(username=user_name).first()
        user_emailid_exists = User.query.filter_by(user_emailid=user_emailid).first()

        admin_name_exists = AdminDB.query.filter_by(admin_username=user_name).first()
        admin_emailid_exists = AdminDB.query.filter_by(admin_emailid=user_emailid).first()

        qs_name_exists = QuestionSetter.query.filter_by(question_setter_username=user_name).first()
        qs_emailid_exists = QuestionSetter.query.filter_by(question_setter_emailid=user_emailid).first()

        if user_password != user_confirmed_password:
            print("Please type correct confirmed password")
            return redirect(url_for('signup_page'))
        elif user_name_exists is not None or user_emailid_exists is not None or admin_name_exists is not None or admin_emailid_exists is not None or qs_name_exists is not None or qs_emailid_exists is not None:
            print("User with the given credentials already exists")
            return redirect(url_for('homepage.html'))
        elif user_name_exists is None and user_emailid_exists is None:
            user_db_obj = User(user_name, user_emailid, user_first_name, user_last_name, user_created_at,
                               hashed_password)
            db.session.add(user_db_obj)
            db.session.commit()

            new_user_data = User.query.filter_by(username=user_name).first()
            login_user(user=new_user_data, remember=True)
            return redirect(url_for('views.home'))
    else:
        return render_template('signup_page.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.homepage'))

