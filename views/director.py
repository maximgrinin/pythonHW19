# Здесь контроллеры/хендлеры/представления для обработки запросов (flask ручки).
# Сюда импортируются сервисы из пакета service
from flask import request
from flask_restx import Resource, Namespace
from dao.model.director import DirectorSchema
from decorator import auth_required, admin_required
from implemented import director_service

director_ns = Namespace('directors')

# Создаем экземпляры схем сериализации для одной и нескольких сущностей
director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


# Функции API для режиссеров - /directors/
@director_ns.route('/')
class DirectorsView(Resource):
    @auth_required
    def get(self):
        all_directors = director_service.get_all()
        # Если результаты запроса - пустые - говорим что данные не найдены
        if not all_directors:
            return f'Результаты запроса не найдены', 404
        return directors_schema.dump(all_directors), 200

    @admin_required
    def post(self):
        req_json = request.json
        if not req_json:
            return 'Ошибка при получении информации о новом режиссере', 404
        director_service.create(req_json)
        return "", 201


# Функции API для единичного экземпляра - режиссера - /directors/<int:uid>
@director_ns.route('/<int:uid>')
class DirectorView(Resource):
    @auth_required
    def get(self, uid):
        try:
            director = director_service.get_one(uid)
            return director_schema.dump(director), 200
        except Exception as e:
            return f'Режиссер по указанному id = {uid} не найден - {str(e)}', 404

    @admin_required
    def put(self, uid):
        try:
            req_json = request.json
            director_service.update(uid, req_json)
            return "", 204
        except Exception as e:
            return f'Режиссер по указанному id = {uid} не найден - {str(e)}', 404

    @admin_required
    def patch(self, uid):
        try:
            req_json = request.json
            director_service.update(uid, req_json)
            return "", 204
        except Exception as e:
            return f'Режиссер по указанному id = {uid} не найден - {str(e)}', 404

    @admin_required
    def delete(self, uid):
        try:
            director_service.delete(uid)
        except Exception as e:
            return f'Режиссер по указанному id = {uid} не найден - {str(e)}', 404
