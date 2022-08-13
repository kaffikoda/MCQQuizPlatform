from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_manager, current_user
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class User(db.Model, UserMixin):
    __tablename__ = "user_table"

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

    def get_id(self):
        return self.username

    def __repr__(self):
        return '<User %r>' % self.username


class AdminDB(db.Model, UserMixin):
    __tablename__ = "admin_table"

    admin_id = db.Column(db.Integer, primary_key=True)
    admin_username = db.Column(db.String(80), unique=True, nullable=False)
    admin_emailid = db.Column(db.String(120), unique=True, nullable=False)
    admin_first_name = db.Column(db.String(80), nullable=False)
    admin_last_name = db.Column(db.String(80), nullable=False)
    admin_created_at = db.Column(db.DateTime, nullable=False)
    hashed_password = db.Column(db.String(128), nullable=False)

    def __init__(self, admin_username, admin_emailid, admin_first_name, admin_last_name, admin_created_at,
                 hashed_password):
        self.admin_username = admin_username
        self.admin_emailid = admin_emailid
        self.admin_first_name = admin_first_name
        self.admin_last_name = admin_last_name
        self.admin_created_at = admin_created_at
        self.hashed_password = hashed_password

    def get_id(self):
        return self.admin_username

    def __repr__(self):
        return '<Admin %r>' % self.admin_username


class QuestionSetter(db.Model, UserMixin):
    __tablename__ = "question_setter"

    question_setter_id = db.Column(db.Integer, primary_key=True)
    question_setter_username = db.Column(db.String(80), unique=True, nullable=False)
    question_setter_emailid = db.Column(db.String(120), unique=True, nullable=False)
    question_setter_first_name = db.Column(db.String(80), nullable=False)
    question_setter_last_name = db.Column(db.String(80), nullable=False)
    question_setter_created_at = db.Column(db.DateTime, nullable=False)
    hashed_password = db.Column(db.String(128), nullable=False)
    quiz_by_question_setter = db.relationship("QuizDetails")

    def __init__(self, question_setter_username, question_setter_emailid, question_setter_first_name,
                 question_setter_last_name, question_setter_created_at, hashed_password):
        self.question_setter_username = question_setter_username
        self.question_setter_emailid = question_setter_emailid
        self.question_setter_first_name = question_setter_first_name
        self.question_setter_last_name = question_setter_last_name
        self.question_setter_created_at = question_setter_created_at
        self.hashed_password = hashed_password

    def get_id(self):
        return self.question_setter_username

    def get_qid(self):
        return self.question_setter_id

    def __repr__(self):
        return '<QuestionSetter %r>' % self.question_setter_username


class QuizDetails(db.Model):
    __tablename__ = "quiz_details"

    quiz_id = db.Column(db.Integer, primary_key=True)
    quiz_made_by = db.Column(db.Integer, db.ForeignKey("question_setter.question_setter_id"), nullable=False)
    quiz_created_at = db.Column(db.DateTime, nullable=False)
    quiz_name = db.Column(db.String(80), nullable=False)
    quiz_question = db.relationship("QuizQuestions")
    questions_attempted = db.relationship("QuestionAttemptedDB")

    def __init__(self, quiz_made_by, quiz_created_at, quiz_name):
        self.quiz_made_by = quiz_made_by
        self.quiz_created_at = quiz_created_at
        self.quiz_name = quiz_name

    # def get_quiz_id(self):
    #     return self.quiz_id


class QuizQuestions(db.Model):
    __tablename__ = "quiz_questions"

    question_id = db.Column(db.Integer, primary_key=True)
    question_quiz_id = db.Column(db.Integer, db.ForeignKey("quiz_details.quiz_id"), nullable=False)
    question = db.Column(db.String(128), nullable=False)
    first_option = db.Column(db.String(128), nullable=False)
    second_option = db.Column(db.String(128), nullable=False)
    third_option = db.Column(db.String(128), nullable=False)
    fourth_option = db.Column(db.String(128), nullable=False)
    correct_answer = db.Column(db.Integer, nullable=False)
    question_created_at = db.Column(db.DateTime, nullable=False)
    question_setter_id = db.Column(db.Integer, nullable=False)

    def __init__(self, question_quiz_id, question, first_option, second_option, third_option, fourth_option,
                 correct_answer, question_created_at, question_setter_id):
        self.question_quiz_id = question_quiz_id
        self.question = question
        self.first_option = first_option
        self.second_option = second_option
        self.third_option = third_option
        self.fourth_option = fourth_option
        self.correct_answer = correct_answer
        self.question_created_at = question_created_at
        self.question_setter_id = question_setter_id


class AttemptedDB(db.Model):
    __tablename__ = "quiz_attempted"

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz_details.quiz_id"), nullable=False)
    quiz_attempted_by = db.Column(db.Integer, nullable=True)
    attempted_at = db.Column(db.DateTime, nullable=False)
    quiz_score = db.Column(db.Integer, nullable=True)
    quiz_by_question_setter = db.relationship("QuizDetails")

    def __init__(self, quiz_id, quiz_attempted_by, attempted_at):
        self.quiz_id = quiz_id
        self.quiz_attempted_by = quiz_attempted_by
        self.attempted_at = attempted_at
        self.quiz_score = 0


class QuestionAttemptedDB(db.Model):
    __tablename__ = "questions_attempted"

    id = db.Column(db.Integer, primary_key=True)
    attempted_quiz_id = db.Column(db.Integer, db.ForeignKey("quiz_details.quiz_id"), nullable=False)
    quiz_attempted_by = db.Column(db.Integer, nullable=False)
    quiz_question_id = db.Column(db.Integer, nullable=False)
    correct_answer = db.Column(db.Integer, nullable=False)
    answer_given = db.Column(db.Integer, nullable=False)
    total_score = db.Column(db.Integer, nullable=False)
    quiz_attempted = db.relationship("QuizDetails")

    def __init__(self, attempted_quiz_id, quiz_attempted_by, quiz_question_id, correct_answer, answer_given):
        self.attempted_quiz_id = attempted_quiz_id
        self.quiz_attempted_by = quiz_attempted_by
        self.quiz_question_id = quiz_question_id
        self.correct_answer = correct_answer
        self.answer_given = answer_given
        self.total_score = 0
