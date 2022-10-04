# Здесь контроллеры/хендлеры/представления для обработки запросов (flask ручки).
# Сюда импортируются сервисы из пакета service
from flask import request
from flask_restx import Resource, Namespace
from implemented import auth_service

auth_ns = Namespace('auth')


# Функции API для авторизации
@auth_ns.route('/')
class AuthsView(Resource):
    def post(self):
        req_json = request.json
        if not req_json:
            return 'Ошибка при получении информации при авторизации', 404

        username = req_json.get('username', None)
        password = req_json.get('password', None)
        if None in [username, password]:
            return '', 400

        tokens = auth_service.generate_tokens(username, password)
        return tokens, 201

    def put(self):
        req_json = request.json
        token = req_json.get("refresh_token")
        try:
            tokens = auth_service.approve_refresh_token(token)
            return tokens, 201
        except Exception as e:
            return f'Ошибка авторизации, {str(e)}', 401
