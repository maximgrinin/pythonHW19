# Основной файл приложения.
# Здесь конфигурируется фласк, сервисы, SQLAlchemy и все остальное что требуется для приложения.
from flask import Flask
from flask_restx import Api
from config import Config
from setup_db import db
from views.director import director_ns
from views.genre import genre_ns
from views.movie import movie_ns
from views.user import user_ns
from views.auth import auth_ns


# Функция создания основного объекта app
def create_app(config_object: Config) -> Flask:
    application = Flask(__name__)
    application.config.from_object(config_object)
    register_extensions(application)
    # application.app_context().push()
    return application


# Функция подключения расширений (Flask-SQLAlchemy, Flask-RESTx, ...)
def register_extensions(application):
    db.init_app(application)
    api = Api(application)
    api.add_namespace(movie_ns)
    api.add_namespace(director_ns)
    api.add_namespace(genre_ns)
    api.add_namespace(user_ns)
    api.add_namespace(auth_ns)
    # with application.app_context():
    #     db.create_all()


if __name__ == '__main__':
    app = create_app(Config())
    app.run(host="localhost", port=10001)
