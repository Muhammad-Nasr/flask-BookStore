import os

class BaseConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
<<<<<<< HEAD
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
=======
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace(
        'postgres://', 'postgresql://')
>>>>>>> d0e5015e071f3fc2e63e0575d2c4474b1c333dd5
    SQLALCHEMY_TRACK_MODIFICATIONS = False
