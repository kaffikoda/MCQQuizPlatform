from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)



@app.route('/user_registration', methods=['GET', 'POST'])
def user_registration():
    user_name = request.form.get('new_username')
    user_emailid = request.form.get('new_email')


    return render_template('user_registration.html')


if __name__ == "__main__":
    app.run(debug=True)
