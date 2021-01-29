# Importaciones del sistema
import os
# Importaciones de Flask o librerias a fin
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_ckeditor import CKEditor
from flask_talisman import Talisman

# Inicializamos SQLAlchemy en la variable db
db = SQLAlchemy()
# Unicializamos la variable migrate
migrate = Migrate()
ckeditor = CKEditor()
talisman = Talisman()
# La funcion principal que define nuestra app y sus propiedades
def create_app(test_config=None):
    # Creacion de la app
    app = Flask(__name__, instance_relative_config=True)
    # Configuraciones de la app
    app.config.from_mapping(
        SECRET_KEY = os.environ.get('SECRET_KEY'),
        SQLALCHEMY_DATABASE_URI= os.environ.get('DATABASE_URL'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        # Email
        MAIL_SERVER='smtp.googlemail.com',
        MAIL_PORT= 587,
        MAIL_USE_TLS= True,
        MAIL_USE_SSL= False,
        MAIL_USERNAME=os.environ.get('MAIL_USERNAME'),
        MAIL_PASSWORD= os.environ.get('MAIL_PASSWORD'),
        MAIL_DEFAULT_SENDER=os.environ.get('MAIL_DEFAULT_SENDER'),
        MAIL_MAX_EMAILS=None,
        MAIL_ASCII_ATTACHMENTS =False,
        # AWS
        S3_BUCKET=os.environ.get('S3_BUCKET_NAME'),
        S3_KEY=os.environ.get('AWS_ACCESS_KEY'),
        S3_SECRET=os.environ.get('AWS_ACCESS_SECRET'),
        S3_LOCATION=os.environ.get('S3_LOCATION'),
        # ckeditor
        CKEDITOR_PKG_TYPE='standard',
    )

    # Condicion para definir el test de nuestra app
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

    # Rutas principales de nuestra app
    @app.route('/')
    def index():
        return render_template('index.html')
    @app.route('/about')
    def about():
        return render_template("about.html")
    @app.route('/cv')
    def cv():
        return redirect(url_for('static', filename='Hector-ulises-gonzalez-medel.pdf'))

    # Rutas de errores de nuestra app
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def page_not_found(e):
        return render_template('500.html'), 500

    # Importamos nuestro modelo user desde nuestro archivo models
    from .models import User
    # Funcion que liga nuestro login con nuestra app
    login_manager = LoginManager()
    # Definir que ruta se encargara de nuestro login en la biblioteca flask-login
    login_manager.login_view = 'auth.login'
    # Inicializamos login manager con nuestra app
    login_manager.init_app(app)
    ckeditor.init_app(app)

    # Definimos a nuestro usuario de flask-login como la sesion activa
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Importamos nuestros blueprints
    from . import auth, blog, workshop, portafolio, email

    # Ligamos nuestra base de datos con la app
    db.init_app(app)
    # Ligamos la funcion migrate de flask-migrate con la app
    migrate.init_app(app,db)
    talisman.init_app(app)
    # Registramos nuestros blueprints
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(workshop.bp)
    app.register_blueprint(portafolio.bp)
    app.register_blueprint(email.bp)

    return app
