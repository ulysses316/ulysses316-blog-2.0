import os

from flask import Flask, render_template, redirect, url_for
from flask_mail import Mail

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = os.environ.get('SECRET_KEY'),
        DATABASE = os.path.join(app.instance_path, 'blog.sqlite'),
        UPLOAD_FOLDER = os.path.join(app.static_folder, 'upload'),
        MAIL_SERVER='smtp.googlemail.com',
        MAIL_PORT= 587,
        MAIL_USE_TLS= True,
        MAIL_USE_SSL= False,
        MAIL_USERNAME=os.environ.get('MAIL_USERNAME'),
        MAIL_PASSWORD= os.environ.get('MAIL_PASSWORD'),
        MAIL_DEFAULT_SENDER='joedoefirebase@gmail.com',
        MAIL_MAX_EMAILS=None,
        MAIL_ASCII_ATTACHMENTS =False,
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def index():
        return render_template('index.html')
    @app.route('/about')
    def about():
        return render_template("about.html")
    @app.route('/cv')
    def cv():
        return redirect(url_for('static', filename='Hector-ulises-gonzalez-medel.pdf'))

    from . import db, auth, blog, workshop, portafolio, email
    db.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(workshop.bp)
    app.register_blueprint(portafolio.bp)
    app.register_blueprint(email.bp)
    return app
