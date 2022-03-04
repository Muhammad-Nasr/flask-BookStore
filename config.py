import os

class BaseConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:123456@localhost/book_store"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
