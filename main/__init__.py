from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import BaseConfig
from flask_login import LoginManager
from flask_moment import Moment
from flask_admin import Admin

bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
moment = Moment()
admin = Admin()

def create_app(config_class=BaseConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)

    admin.init_app(app, index_view=models.MyAdminIndexView())

    from main.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from main.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from main.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app


from main import models