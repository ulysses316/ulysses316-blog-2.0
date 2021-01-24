import os
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# Inicializamos SQLAlchemy en la variable db
db = SQLAlchemy()
migrate = Migrate()

# La funcion principal que define todas las propiedades de nuestra app
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = os.environ.get('SECRET_KEY'),
        SQLALCHEMY_DATABASE_URI= os.environ.get('DATABASE_URL'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        UPLOAD_FOLDER = os.path.join(app.static_folder, 'upload'),
        MAIL_SERVER='smtp.googlemail.com',
        MAIL_PORT= 587,
        MAIL_USE_TLS= True,
        MAIL_USE_SSL= True,
        MAIL_USERNAME=os.environ.get('MAIL_USERNAME'),
        MAIL_PASSWORD= os.environ.get('MAIL_PASSWORD'),
        MAIL_DEFAULT_SENDER=os.environ.get('MAIL_DEFAULT_SENDER'),
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

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def page_not_found(e):
        return render_template('500.html'), 500

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from . import auth, blog, workshop, portafolio, email
    db.init_app(app)
    migrate.init_app(app,db)

    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(workshop.bp)
    app.register_blueprint(portafolio.bp)
    app.register_blueprint(email.bp)
    return app
