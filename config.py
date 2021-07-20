import os
basedir =  os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY'),
    SQLALCHEMY_TRACK_MODIFICATIONS = False,
    # Email
    MAIL_SERVER = 'smtp.googlemail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME'),
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD'),
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER'),
    MAIL_MAX_EMAILS = None,
    MAIL_ASCII_ATTACHMENTS = False,
    # AWS
    S3_BUCKET = os.environ.get('S3_BUCKET_NAME'),
    S3_KEY = os.environ.get('AWS_ACCESS_KEY'),
    S3_SECRET = os.environ.get('AWS_ACCESS_SECRET'),
    S3_LOCATION = os.environ.get('S3_LOCATION'),
    # ckeditor
    CKEDITOR_PKG_TYPE = 'standard',

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True,
    SECRET_KEY = 'dev',
    UPLOAD_FOLDER = os.path.join(app.static_folder, 'upload'),
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance/data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI= os.environ.get('DATABASE_URL'),