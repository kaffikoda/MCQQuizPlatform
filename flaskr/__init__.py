from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os

load_dotenv()
db = SQLAlchemy()
# DB_NAME = os.environ.get('DB_NAME')


# def init_db(app):
#     db.init_app(app)
#     db.app = app
#     db.create_all()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, AdminDB, QuestionSetter, QuizDetails, QuizQuestions, QuestionAttemptedDB, AttemptedDB

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        if AdminDB.query.filter_by(admin_username=id).first() is not None:
            return AdminDB.query.filter_by(admin_username=id).first()
        elif QuestionSetter.query.filter_by(question_setter_username=id).first() is not None:
            return QuestionSetter.query.filter_by(question_setter_username=id).first()
        return User.query.filter_by(username=id).first()

    return app
