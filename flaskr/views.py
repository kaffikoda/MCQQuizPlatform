from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from .models import QuestionSetter, QuizQuestions, QuizDetails, User, AttemptedDB, QuestionAttemptedDB
from . import db
from sqlalchemy import and_

views = Blueprint("views", __name__)

qu = []
ATTEMPTED_QUESTIONS_LIST = []
QUESTIONS_CREATED_TILLNOW = []


@views.route('/')
def homepage():
    return redirect(url_for('auth.login'))


@views.route('/home', methods=["GET"])  # takes to the home
def home():
    if isinstance(current_user, QuestionSetter) and current_user.is_authenticated:
        return redirect(url_for('views.created_quizzes'))
    elif isinstance(current_user, User) and current_user.is_authenticated:
        return redirect(url_for('views.available_quizzes'))

    return redirect(url_for('views.add_questionsetter'))


@views.route('/add_questionsetter', methods=["GET", "POST"])  # admin adds question setter
def add_questionsetter():
    # print(current_user)
    if request.method == "POST":
        question_setter_username = request.form.get("inputQSUserName")
        question_setter_emailid = request.form.get("inputQSEmail")
        question_setter_first_name = request.form.get("inputQSFirstName")
        question_setter_last_name = request.form.get("inputQSLastName")
        question_setter_created_at = datetime.now()
        question_setter_password = request.form.get("inputQSPassword")
        question_setter_confirmed_password = request.form.get("inputQSConfirmPassword")
        hashed_password = generate_password_hash(question_setter_password)

        qs_search_username = QuestionSetter.query.filter_by(question_setter_username=question_setter_username).first()
        qs_search_email = QuestionSetter.query.filter_by(question_setter_emailid=question_setter_emailid).first()

        # print(qs_search_email)
        # print(qs_search_username)

        if question_setter_password != question_setter_confirmed_password:
            print("Please type correct confirmed password")
            return redirect(url_for('views.add_questionsetter'))
        elif qs_search_username is None and qs_search_email is None:
            question_setter_obj = QuestionSetter(question_setter_username, question_setter_emailid,
                                                 question_setter_first_name, question_setter_last_name,
                                                 question_setter_created_at, hashed_password)
            db.session.add(question_setter_obj)
            db.session.commit()
        elif qs_search_username is not None or qs_search_email is not None:
            print("Question setter with the given data already exists")

    return render_template('add_questionsetter.html')


@views.route('/create_quiz', methods=["POST"])  # will be called when a question setter creates a new quiz
def create_quiz():
    quiz_details_obj = QuizDetails(current_user.get_qid(), quiz_created_at=datetime.now(),
                                   quiz_name=request.form.get("quizName"))
    db.session.add(quiz_details_obj)
    db.session.commit()

    return redirect(url_for('views.create_questions', quiz_id=quiz_details_obj.quiz_id))


@views.route('/create_question/<int:quiz_id>', methods=["GET", "POST"])  # creating questions for the quiz
def create_questions(quiz_id):
    questions_created_tillnow_obj = QuizQuestions.query.filter_by(question_quiz_id=quiz_id)
    print(ATTEMPTED_QUESTIONS_LIST)

    if request.method == "POST" and "addQuestion" in request.form:
        entered_question = request.form.get('inputQuestion')
        first_option = request.form.get('option1')
        second_option = request.form.get('option2')
        third_option = request.form.get('option3')
        fourth_option = request.form.get('option4')
        correct_option = request.form.get('correctOption')

        print(request.form.get("correctOption"))

        quiz_details_obj = QuizDetails.query.filter_by(quiz_id=quiz_id).first()

        question_obj = QuizQuestions(question_quiz_id=quiz_id, question=entered_question,
                                     first_option=first_option, second_option=second_option, third_option=third_option,
                                     fourth_option=fourth_option, correct_answer=correct_option,
                                     question_created_at=datetime.now(),
                                     question_setter_id=quiz_details_obj.quiz_made_by)
        db.session.add(question_obj)
        db.session.commit()

        return redirect(url_for('views.create_questions', quiz_id=quiz_id))

    if questions_created_tillnow_obj is None:
        return render_template('create_quiz.html')

    questions_created_tillnow_list = [ques for ques in questions_created_tillnow_obj]
    number_of_questions = questions_created_tillnow_obj.count()

    return render_template('create_quiz.html', questions_created_tillnow_list=questions_created_tillnow_list,
                           number_of_questions=number_of_questions,
                           questions_created_tillnow_obj=questions_created_tillnow_obj)


@views.route('/delete_question/<int:quiz_id>/<int:question_id>',
             methods=["GET", "POST"])  # deleting a question in a quiz
def delete_question(quiz_id, question_id):
    delete_obj = QuizQuestions.query.filter_by(question_id=question_id).first()
    db.session.delete(delete_obj)
    db.session.commit()

    return redirect(url_for('views.create_questions', quiz_id=quiz_id))


@views.route('/edit_question/<int:quiz_id>/<int:question_id>', methods=["POST"])  # editing a question in a quiz
def edit_question(quiz_id, question_id):
    questions_obj = db.session.query(QuizQuestions).get(question_id)

    # print(questions_obj.question, "-", questions_obj.first_option, "-", questions_obj.second_option, "-",
    #       questions_obj.correct_answer)

    # print(request.form.get("correctOption"))

    questions_obj.question = request.form.get('editedQuestion')
    questions_obj.first_option = request.form.get('option1')
    questions_obj.second_option = request.form.get('option2')
    questions_obj.third_option = request.form.get('option3')
    questions_obj.fourth_option = request.form.get('option4')
    questions_obj.correct_answer = int(request.form.get('correctOption'))

    print(request.form.get('correctOption'))

    db.session.commit()

    global qu
    qu = db.session.query(QuizQuestions).filter_by(question_quiz_id=quiz_id)

    return redirect(url_for('views.create_questions', quiz_id=quiz_id))


@views.route('/available_quizzes', methods=["GET"])  # tells which quizzes are available for a user
def available_quizzes():
    quiz_attempted_by_user = AttemptedDB.query.filter_by(quiz_attempted_by=current_user.user_id)
    quiz_attempted_by_user_list = [details.quiz_id for details in quiz_attempted_by_user]

    all_quizzes_available = QuizDetails.query.all()

    return render_template('available_quizzes.html', quiz_attempted_by_user_list=quiz_attempted_by_user_list,
                           all_quizzes_available=all_quizzes_available, total_number_of_quizzes=len(all_quizzes_available))


@views.route('/play_quiz/<int:quiz_id>', methods=["GET", "POST"])  # will be called when user is attempting a quiz
def play_quiz(quiz_id):
    questions = QuizQuestions.query.filter_by(question_quiz_id=quiz_id)

    number_of_questions = questions.count()

    attempted_or_not = AttemptedDB.query.filter(
        and_(AttemptedDB.quiz_id == quiz_id, AttemptedDB.quiz_attempted_by == current_user.user_id)).first()

    attempted_questions = QuestionAttemptedDB.query.filter(and_(QuestionAttemptedDB.attempted_quiz_id == quiz_id,
                                                                QuestionAttemptedDB.quiz_attempted_by == current_user.user_id))

    if attempted_or_not is None:
        quiz_attempted_obj = AttemptedDB(quiz_id=quiz_id, quiz_attempted_by=current_user.user_id,
                                         attempted_at=datetime.now())
        db.session.add(quiz_attempted_obj)
        db.session.commit()

    if request.method == "POST":
        if "submitAnswer" in request.form:
            correct_answer = db.session.query(QuizQuestions).get(request.form.get("submitAnswer")).correct_answer
            answer_given = int(request.form.get("selectedOption"))

            question_attempted_obj = QuestionAttemptedDB(attempted_quiz_id=quiz_id,
                                                         quiz_attempted_by=current_user.user_id,
                                                         quiz_question_id=int(request.form.get("submitAnswer")),
                                                         correct_answer=correct_answer, answer_given=answer_given)

            if correct_answer == answer_given:
                question_attempted_obj.total_score = 1

            db.session.add(question_attempted_obj)
            db.session.commit()

            global ATTEMPTED_QUESTIONS_LIST
            ATTEMPTED_QUESTIONS_LIST = [ques.quiz_question_id for ques in attempted_questions]

            print(ATTEMPTED_QUESTIONS_LIST)

            return redirect(url_for('views.play_quiz', quiz_id=quiz_id))
        elif "submitQuiz" in request.form:
            questions_attempted_by_user_obj = QuestionAttemptedDB.query.filter(
                and_(QuestionAttemptedDB.attempted_quiz_id == quiz_id,
                     QuestionAttemptedDB.quiz_attempted_by == current_user.user_id))

            total_score = 0
            for ques in questions_attempted_by_user_obj:
                if ques.answer_given == ques.correct_answer:
                    total_score += 1

            # print("Hello!!!!", total_score)

            quiz_attempted_by_user_obj = AttemptedDB.query.filter(
                and_(AttemptedDB.quiz_id == quiz_id, AttemptedDB.quiz_attempted_by == current_user.user_id)).first()
            quiz_attempted_by_user_obj.quiz_score = total_score
            db.session.commit()

            # print(quiz_attempted_by_user_obj.quiz_score)

            return redirect(url_for('views.home'))

    return render_template('play_quiz.html', questions=questions, number_of_questions=number_of_questions,
                           attempted_questions_list=ATTEMPTED_QUESTIONS_LIST, quiz_id=quiz_id)


@views.route('/attempted_quizzes', methods=["GET"])  # tells which quizzes the user has attempted
def attempted_quizzes():
    quiz_attempted_by_user = AttemptedDB.query.filter_by(quiz_attempted_by=current_user.user_id)
    attempted_by_user_list = [details.quiz_id for details in quiz_attempted_by_user]

    all_quizzes_available = QuizDetails.query.all()

    return render_template('attempted_quizzes.html', all_quizzes_available=all_quizzes_available,
                           attempted_by_user_list=attempted_by_user_list, flag=0,
                           total_number_of_quizzes=len(all_quizzes_available))


@views.route('/questions/<int:quiz_id>', methods=["GET"])  # shows the response oo the user and the content made by
# the questionsetter
def show_questions(quiz_id):
    questions_details_obj = QuizQuestions.query.filter_by(question_quiz_id=quiz_id)
    number_of_questions = questions_details_obj.count()

    if isinstance(current_user, User):
        attempt_by_user_obj = QuestionAttemptedDB.query.filter(and_(QuestionAttemptedDB.attempted_quiz_id == quiz_id,
                                                                    QuestionAttemptedDB.quiz_attempted_by == current_user.user_id))
        questions_attempted_by_user_dict = {quiz.quiz_question_id: quiz.answer_given for quiz in attempt_by_user_obj}

        quiz_attempted_by_user = AttemptedDB.query.filter(
            and_(AttemptedDB.quiz_id == quiz_id, AttemptedDB.quiz_attempted_by == current_user.user_id)).first()

        print(quiz_attempted_by_user)

        return render_template('show_questions.html', questions_attempted_by_user_dict=questions_attempted_by_user_dict,
                               number_of_questions=number_of_questions, questions_details_obj=questions_details_obj,
                               questions_attempted_details=attempt_by_user_obj, flag=0,
                               user_score=quiz_attempted_by_user.quiz_score)

    return render_template('show_questions.html', questions_details_obj=questions_details_obj,
                           number_of_questions=number_of_questions, flag=1)


@views.route('/created_quizzes', methods=["GET"])  # tells about the quizzes made by the questionsetter
def created_quizzes():
    quiz_created_by_qs = QuizDetails.query.filter_by(quiz_made_by=current_user.question_setter_id)

    return render_template('question_setter_page.html', all_quizzes_available=quiz_created_by_qs, number_of_quizzes=quiz_created_by_qs.count())
