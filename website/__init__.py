from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from os import path, makedirs
import os
from flask_login import LoginManager
from flask_mail import Mail

DB_NAME = "sqlite3.db"
db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "sivasiva"
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    app.config['UPLOAD_FOLDER'] = os.path.join('website','static', 'uploads')
    db.init_app(app)


    app.config["MAIL_SERVER"] = 'smtp.gmail.com'
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USERNAME"]= "sivashiv08@gmail.com"
    app.config["MAIL_PASSWORD"] = "jaxa zodc isme ufji"
    app.config["MAIL_DEFAULT_SENDER"] = "sivashiv08@gmail.com"
    mail.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, urlprefix='/')
    app.register_blueprint(auth, urlprefix='/')

    from .models import User

    create_database(app)
    create_upload_folder(app)

    loginmanager = LoginManager()
    loginmanager.login_view = 'auth.login'
    loginmanager.init_app(app)

    @loginmanager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists("website/" +DB_NAME):
        with app.app_context():
            db.create_all()
        print("database created succesfully")
def create_upload_folder(app):
    if not path.exists(app.config['UPLOAD_FOLDER']):
        makedirs(app.config['UPLOAD_FOLDER'])
        print(f"Uploads folder '{app.config['UPLOAD_FOLDER']}' created successfully")    
    
    