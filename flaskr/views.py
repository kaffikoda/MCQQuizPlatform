from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from .models import QuestionSetter, QuizQuestions, QuizDetails
from . import db

views = Blueprint("views", __name__)

qu = []


@views.route('/')
def homepage():
    return render_template('homepage.html')


@views.route('/home', methods=["GET", "POST"])
def home():
    print(current_user)
    if request.method == "POST":
        question_setter_username = request.form.get("question-setter-username")
        question_setter_emailid = request.form.get("question-setter-email")
        question_setter_first_name = request.form.get("question-setter-first-name")
        question_setter_last_name = request.form.get("question-setter-last-name")
        question_setter_created_at = datetime.now()
        question_setter_password = request.form.get("question-setter-password")
        question_setter_confirmed_password = request.form.get("question-setter-confirm-password")
        hashed_password = generate_password_hash(question_setter_password)

        qs_search_username = QuestionSetter.query.filter_by(question_setter_username=question_setter_username).first()
        qs_search_email = QuestionSetter.query.filter_by(question_setter_emailid=question_setter_emailid).first()

        print(qs_search_email)
        print(qs_search_username)

        if question_setter_password != question_setter_confirmed_password:
            print("Please type correct confirmed password")
            return redirect(url_for('admin_dashboard'))
        elif qs_search_username is None and qs_search_email is None:
            question_setter_obj = QuestionSetter(question_setter_username, question_setter_emailid,
                                                 question_setter_first_name, question_setter_last_name,
                                                 question_setter_created_at, hashed_password)
            db.session.add(question_setter_obj)
            db.session.commit()

    if isinstance(current_user, QuestionSetter) and current_user.is_authenticated:
        return render_template('question_setter_page.html')

    return render_template('admin_dashboard.html')


@views.route('/create-quiz', methods=["GET", "POST"])
def create_quiz():
    if request.method == "POST" and "submitQuizName" in request.form:
        quiz_details_obj = QuizDetails(current_user.get_qid(), quiz_created_at=datetime.now(),
                                       quiz_name=request.form.get("submitQuizName"))
        db.session.add(quiz_details_obj)
        db.session.commit()
        print("Create Quiz!!!!!!!!")
    elif request.method == "POST" and "addQuestion" in request.form:
        entered_question = request.form.get('entered-question')
        first_option = request.form.get('option1')
        second_option = request.form.get('option2')
        third_option = request.form.get('option3')
        fourth_option = request.form.get('option4')
        correct_option = 0

        # if flag == 0:
        #     quiz_details_obj.quiz_made_by = current_user.get_qid()
        #     quiz_details_obj.quiz_name = "Hello Testing"
        #     db.session.add(quiz_details_obj)
        #     db.session.commit()
        #     flag += 1

        quiz_details_obj = db.session.query(QuizDetails).order_by(QuizDetails.quiz_id.desc()).first()
        # question_obj = QuizQuestions(question_quiz_id=quiz_details_obj.quiz_id, question=entered_question, first_option=first_option, second_option=second_option, third_option=third_option, fourth_option=fourth_option, correct_answer=correct_option, question_created_at=datetime.now(), question_setter_id=temp_obj.quiz_made_by)
        # db.session.add(question_obj)
        # db.session.commit()

        print(quiz_details_obj.quiz_id)
        print(quiz_details_obj.quiz_made_by)

        if request.form.get('correctOption') == 'option1':
            correct_option = 1
        elif request.form.get('correctOption') == 'option2':
            correct_option = 2
        elif request.form.get('correctOption') == 'option3':
            correct_option = 3
        else:
            correct_option = 4

        question_obj = QuizQuestions(question_quiz_id=quiz_details_obj.quiz_id, question=entered_question,
                                     first_option=first_option, second_option=second_option, third_option=third_option,
                                     fourth_option=fourth_option, correct_answer=correct_option,
                                     question_created_at=datetime.now(),
                                     question_setter_id=quiz_details_obj.quiz_made_by)
        db.session.add(question_obj)
        db.session.commit()

        # question_obj = QuizQuestions(question_quiz_id=quiz_details_obj.quiz_id, question=entered_question, first_option=first_option, second_option=second_option, third_option=third_option, fourth_option=fourth_option, correct_answer=correct_option, question_created_at=datetime.now(), question_setter_id=100)
        # db.session.add(question_obj)
        # db.session.commit()

        # return render_template("create_quiz.html")

        # print(request.form.get('entered-question'))
        # print(request.form.get('option1'))
        # print(request.form.get('option2'))
        # print(request.form.get('option3'))
        # print(request.form.get('option4'))
        # print(request.form.get('correctOption'))
        # print(request.form.get('quiz-name'))

        # questions_create_tillnow = QuizQuestions.query.filter_by(question_quiz_id=temp_obj.quiz_id).all()

        questions_created_tillnow = db.session.query(QuizQuestions).filter_by(question_quiz_id=quiz_details_obj.quiz_id)

        return render_template('create_quiz.html', questions_created_tillnow=questions_created_tillnow)

    return render_template('create_quiz.html', questions_created_tillnow=qu)


# def create_quiz_details():

@views.route('/delete_question/<int:quiz_id>/<int:question_id>', methods=["POST"])
def delete_question(quiz_id, question_id):
    delete_obj = QuizQuestions.query.filter_by(question_id=question_id).first()
    db.session.delete(delete_obj)
    db.session.commit()

    global qu
    qu = db.session.query(QuizQuestions).filter_by(question_quiz_id=quiz_id)

    # if QuizQuestions.query.filter_by(question_quiz_id=quiz_id).first() is not None:
    #     return render_template('create_quiz.html', questions_created_tillnow=qu)

    return redirect(url_for('views.create_quiz'))


@views.route('/edit_question/<int:quiz_id>/<int:question_id>', methods=["POST"])
def edit_question(quiz_id, question_id):

    questions_obj = db.session.query(QuizQuestions).get(question_id)
    print(questions_obj.question, "-", questions_obj.first_option, "-", questions_obj.second_option, "-")

    questions_obj.question = request.form.get('edited-question')
    questions_obj.first_option = request.form.get('option1')
    questions_obj.second_option = request.form.get('option2')
    questions_obj.third_option = request.form.get('option3')
    questions_obj.fourth_option = request.form.get('option4')
    questions_obj.correct_option = request.form.get('correctOption')
    db.session.commit()

    global qu
    qu = db.session.query(QuizQuestions).filter_by(question_quiz_id=quiz_id)

    return redirect(url_for('views.create_quiz'))




