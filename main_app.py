import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_moment import Moment
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)
from flask_msearch import Search

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"
login_manager.login_message_cartegory = "info"
db = SQLAlchemy()
migrate = Migrate()
moment = Moment()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'secret-key'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///medoc_database.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)
    bcrypt.init_app(app)
    bcrypt.init_app(app)


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from auth.routes import auth

    app.register_blueprint(auth)

    return app
