from flaskr import create_app, db

app = create_app()


def init_db(app):
    db.init_app(app)
    db.app = app
    db.create_all()


init_db(app)

if __name__ == "__main__":
    # init_db(app)
    app.run(debug=True)
