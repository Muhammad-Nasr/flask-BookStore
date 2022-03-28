import os

class BaseConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'how are you'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace(
        'postgres://', 'postgresql://')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
