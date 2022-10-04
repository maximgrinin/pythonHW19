# Здесь контроллеры/хендлеры/представления для обработки запросов (flask ручки).
# Сюда импортируются сервисы из пакета service
from flask import request
from flask_restx import Resource, Namespace
from dao.model.user import UserSchema
from decorator import admin_required
from implemented import user_service

user_ns = Namespace('user')

# Создаем экземпляры схем сериализации для одной и нескольких сущностей
user_schema = UserSchema()
users_schema = UserSchema(many=True)


# Функции API для пользователей - /user/
@user_ns.route('/') # Получение пользователей
class UsersView(Resource):
    @admin_required
    def get(self):
        all_users = user_service.get_all()
        # Если результаты запроса - пустые - говорим что данные не найдены
        if not all_users:
            return f'Результаты запроса не найдены', 404
        return users_schema.dump(all_users), 200

    @admin_required
    def post(self):
        req_json = request.json
        if not req_json:
            return 'Ошибка при получении информации о новом пользователе', 404
        user_service.create(req_json)
        return "", 201


# Функции API для единичного экземпляра - пользователя - /user/<int:uid>
@user_ns.route('/<int:uid>')
class UserView(Resource):
    def get(self, uid):
        try:
            user = user_service.get_one(uid)
            return user_schema.dump(user), 200
        except Exception as e:
            return f'Пользователь по указанному id = {uid} не найден - {str(e)}', 404

    @admin_required
    def put(self, uid):
        try:
            req_json = request.json
            user_service.update(uid, req_json)
            return "", 204
        except Exception as e:
            return f'Пользователь по указанному id = {uid} не найден - {str(e)}', 404

    @admin_required
    def patch(self, uid):
        try:
            req_json = request.json
            user_service.update(uid, req_json)
            return "", 204
        except Exception as e:
            return f'Пользователь по указанному id = {uid} не найден - {str(e)}', 404

    @admin_required
    def delete(self, uid):
        try:
            user_service.delete(uid)
        except Exception as e:
            return f'Пользователь по указанному id = {uid} не найден - {str(e)}', 404
