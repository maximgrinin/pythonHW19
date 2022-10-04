# Здесь контроллеры/хендлеры/представления для обработки запросов (flask ручки).
# Сюда импортируются сервисы из пакета service
from flask import request
from flask_restx import Resource, Namespace
from dao.model.movie import MovieSchema
from decorator import auth_required, admin_required
from implemented import movie_service

# Создаем неймспейс
movie_ns = Namespace('movies')

# Создаем экземпляры схем сериализации для одной и нескольких сущностей
movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


# Функции API для фильмов - /movies/
@movie_ns.route('/')
class MoviesView(Resource):
    @auth_required
    def get(self):
        args = request.args.to_dict()
        all_movies = movie_service.get_all(args)
        # Если результаты запроса - пустые - говорим что данные не найдены
        if not all_movies:
            return f'Результаты запроса не найдены', 404
        return movies_schema.dump(all_movies), 200

    @admin_required
    def post(self):
        req_json = request.json
        if not req_json:
            return 'Ошибка при получении информации о новом фильме', 404
        movie_service.create(req_json)
        return "", 201


# Функции API для единичного экземпляра - фильма - /movies/<int:uid>
@movie_ns.route('/<int:uid>')
class MovieView(Resource):
    @auth_required
    def get(self, uid):
        try:
            movie = movie_service.get_one(uid)
            return movie_schema.dump(movie), 200
        except Exception as e:
            return f'Фильм по указанному id = {uid} не найден - {str(e)}', 404

    @admin_required
    def put(self, uid):
        try:
            req_json = request.json
            movie_service.update(uid, req_json)
            return "", 204
        except Exception as e:
            return f'Фильм по указанному id = {uid} не найден - {str(e)}', 404

    @admin_required
    def patch(self, uid):
        try:
            req_json = request.json
            movie_service.update(uid, req_json)
            return "", 204
        except Exception as e:
            return f'Фильм по указанному id = {uid} не найден - {str(e)}', 404

    @admin_required
    def delete(self, uid):
        try:
            movie_service.delete(uid)
        except Exception as e:
            return f'Фильм по указанному id = {uid} не найден - {str(e)}', 404
