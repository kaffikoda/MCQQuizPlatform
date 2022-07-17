from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/user_registration', methods=["GET", "POST"])
def signup_page():
    if request.method == "POST":
        # user_name = request.form["new_username"]
        # user_emailid = request.form["new_email"]

        user_name = request.form.get("new_username")
        user_emailid = request.form.get("new_email")

        # print(user_name + " " + user_emailid)

        return render_template('homepage.html')
    else:
        return render_template('signup_page.html')


if __name__ == "__main__":
    app.run(debug=True)
