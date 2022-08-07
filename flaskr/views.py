from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from .models import QuestionSetter, QuizQuestions, QuizDetails, User, AttemptedDB, QuestionAttemptedDB
from . import db
from sqlalchemy import and_

views = Blueprint("views", __name__)

qu = []

attempted_questions_list = []


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
    elif isinstance(current_user, User) and current_user.is_authenticated:
        return render_template('user_page.html')

    return render_template('admin_dashboard.html')


@views.route('/create-quiz', methods=["GET", "POST"])
def create_quiz():
    if request.method == "POST" and "submitQuizName" in request.form:
        quiz_details_obj = QuizDetails(current_user.get_qid(), quiz_created_at=datetime.now(),
                                       quiz_name=request.form.get("quizName"))
        db.session.add(quiz_details_obj)
        db.session.commit()
        print("Create Quiz!!!!!!!!")
    elif request.method == "POST" and "addQuestion" in request.form:
        entered_question = request.form.get('entered-question')
        first_option = request.form.get('option1')
        second_option = request.form.get('option2')
        third_option = request.form.get('option3')
        fourth_option = request.form.get('option4')
        correct_option = int(request.form.get('correctOption'))

        print(request.form.get("correctOption"))

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

        # if request.form.get('correctOption') == 'option1':
        #     correct_option = 1
        # elif request.form.get('correctOption') == 'option2':
        #     correct_option = 2
        # elif request.form.get('correctOption') == 'option3':
        #     correct_option = 3
        # else:
        #     correct_option = 4

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
    # print(db.session.query(QuizQuestions).filter_by(question_quiz_id=quiz_id))
    # print(QuizQuestions.query.filter_by(question_quiz_id=quiz_id))
    # print(qu)

    # for temp in qu:
    #     print(temp.question_quiz_id)

    # if QuizQuestions.query.filter_by(question_quiz_id=quiz_id).first() is not None:
    #     return render_template('create_quiz.html', questions_created_tillnow=qu)

    return redirect(url_for('views.create_quiz'))


@views.route('/edit_question/<int:quiz_id>/<int:question_id>', methods=["POST"])
def edit_question(quiz_id, question_id):
    questions_obj = db.session.query(QuizQuestions).get(question_id)

    print(questions_obj.question, "-", questions_obj.first_option, "-", questions_obj.second_option, "-",
          questions_obj.correct_answer)

    print(request.form.get("correctOption"))

    # if request.form.get('correctOption') == 'option1':
    #     questions_obj.correct_answer = 1
    # elif request.form.get('correctOption') == 'option2':
    #     questions_obj.correct_answer = 2
    # elif request.form.get('correctOption') == 'option3':
    #     questions_obj.correct_answer = 3
    # else:
    #     questions_obj.correct_answer = 4

    questions_obj.question = request.form.get('edited-question')
    questions_obj.first_option = request.form.get('option1')
    questions_obj.second_option = request.form.get('option2')
    questions_obj.third_option = request.form.get('option3')
    questions_obj.fourth_option = request.form.get('option4')
    questions_obj.correct_answer = int(request.form.get('correctOption'))

    db.session.commit()

    global qu
    qu = db.session.query(QuizQuestions).filter_by(question_quiz_id=quiz_id)

    return redirect(url_for('views.create_quiz'))


@views.route('/available_quizzes', methods=["GET"])
def available_quizzes():
    quiz_attempted_by_user = AttemptedDB.query.filter_by(quiz_attempted_by=current_user.user_id)
    quiz_attempted_by_user_list = [details.quiz_id for details in quiz_attempted_by_user]

    all_quizzes_available = QuizDetails.query.all()
    # available_quizzes_for_user = [details.quiz_id for details in all_quizzes_available if details.quiz_id not in quiz_attempted_by_user_list]
    # print(available_quizzes_for_user)

    return render_template('available_quizzes.html', quiz_attempted_by_user_list=quiz_attempted_by_user_list,
                           all_quizzes_available=all_quizzes_available)


@views.route('/play_quiz/<int:quiz_id>', methods=["GET", "POST"])
def play_quiz(quiz_id):
    questions = QuizQuestions.query.filter_by(question_quiz_id=quiz_id)
    # print(type(questions))
    # print("Size:-", questions.count())
    # print(current_user.user_id)

    # print(questions[3].question)

    # empty_list = []
    # print(empty_list)

    number_of_questions = questions.count()

    attempted_or_not = AttemptedDB.query.filter(
        and_(AttemptedDB.quiz_id == quiz_id, AttemptedDB.quiz_attempted_by == current_user.user_id)).first()

    attempted_questions = QuestionAttemptedDB.query.filter(and_(QuestionAttemptedDB.attempted_quiz_id == quiz_id,
                                                                QuestionAttemptedDB.quiz_attempted_by == current_user.user_id))

    # if attempted_questions is not None:
    #     attempted_questions_list = [quiz_id.quiz_question_id for quiz_id in attempted_questions]

    if attempted_or_not is None:
        quiz_attempted_obj = AttemptedDB(quiz_id=quiz_id, quiz_attempted_by=current_user.user_id,
                                         attempted_at=datetime.now())
        db.session.add(quiz_attempted_obj)
        db.session.commit()

    if request.method == "POST" and "submitAnswer" in request.form:
        # print(request.form.get("submitAnswer"))
        # correct_answer = db.session.query(QuizQuestions).get(request.form.get("submitAnswer")).correct_answer
        # print("Hello:-", correct_answer)
        # answer_given = int(request.form.get("selectedOption"))
        # print(type(answer_given))
        # question_attempted = QuestionAttemptedDB(quiz_id, )

        correct_answer = db.session.query(QuizQuestions).get(request.form.get("submitAnswer")).correct_answer
        answer_given = int(request.form.get("selectedOption"))

        question_attempted_obj = QuestionAttemptedDB(attempted_quiz_id=quiz_id, quiz_attempted_by=current_user.user_id,
                                                     quiz_question_id=int(request.form.get("submitAnswer")),
                                                     correct_answer=correct_answer, answer_given=answer_given)

        if correct_answer == answer_given:
            question_attempted_obj.total_score = 1

        db.session.add(question_attempted_obj)
        db.session.commit()

        # attempted_questions = QuestionAttemptedDB.query.filter(and_(QuestionAttemptedDB.attempted_quiz_id ==
        # quiz_id, QuestionAttemptedDB.quiz_attempted_by == current_user.user_id))

        global attempted_questions_list
        attempted_questions_list = [quiz_id.quiz_question_id for quiz_id in attempted_questions]
        # print(attempted_questions)

        # attempted_questions_list = [quiz_id.quiz_question_id for quiz_id in attempted_questions]
        print(attempted_questions_list)

        return render_template('play_quiz.html', questions=questions, number_of_questions=number_of_questions,
                               attempted_questions_list=attempted_questions_list)

    # elif request.method == "POST":
    #     print(request.form)
    #     print(request.form.get('submitAnswer'))
    #
    #     global question_list
    #     question_list.append(int(request.form.get('submitAnswer')))
    #     print(question_list)

    # if attempted_questions is None:
    #     return render_template('play_quiz.html', questions=questions, number_of_questions=number_of_questions)

    return render_template('play_quiz.html', questions=questions, number_of_questions=number_of_questions,
                           attempted_questions_list=attempted_questions_list)


@views.route('/attempted_quizzes', methods=["GET"])
def attempted_quizzes():
    quiz_attempted_by_user = AttemptedDB.query.filter_by(quiz_attempted_by=current_user.user_id)
    attempted_by_user_list = [details.quiz_id for details in quiz_attempted_by_user]

    all_quizzes_available = QuizDetails.query.all()

    return render_template('attempted_quizzes.html', all_quizzes_available=all_quizzes_available,
                           attempted_by_user_list=attempted_by_user_list)


@views.route('/show_attempt/<int:quiz_id>', methods=["GET"])
def show_attempt(quiz_id):
    attempt_by_user_obj = QuestionAttemptedDB.query.filter(and_(QuestionAttemptedDB.attempted_quiz_id == quiz_id,
                                                                QuestionAttemptedDB.quiz_attempted_by == current_user.user_id))

    questions_attempted_by_user_dict = {quiz.quiz_question_id:quiz.answer_given for quiz in attempt_by_user_obj}
    questions_details_obj = QuizQuestions.query.filter_by(question_quiz_id=quiz_id)
    number_of_questions = questions_details_obj.count()
    print(number_of_questions)
    print(attempt_by_user_obj[0].quiz_question_id)

    return render_template('show_attempt.html', questions_attempted_by_user_dict=questions_attempted_by_user_dict,
                           number_of_questions=number_of_questions, questions_details_obj=questions_details_obj,
                           questions_attempted_details=attempt_by_user_obj)
