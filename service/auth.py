# Здесь бизнес логика, в виде классов или методов.
# Сюда импортируются DAO классы из пакета dao и модели из dao.model
# Некоторые методы могут оказаться просто прослойкой между dao и views,
# но чаще всего будет какая-то логика обработки данных сейчас или в будущем.
from service.user import UserService

import calendar
import datetime
import jwt
from flask_restx import abort
from constants import JWT_SECRET, JWT_ALGORITHM


class AuthService:
    def __init__(self, service: UserService):
        self.service = service

    def generate_tokens(self, username, password, is_refresh=False):
        user = self.service.get_by_username(username)
        if user is None:
            raise abort(404)

        if not is_refresh:
            if not self.service.compare_passwords(user.password, password):
                raise abort(400)

        data = {
            "username": user.username,
            "role": user.role
        }

        # Создаем access_token на 30 мин
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

        # Создаем refresh_token на 130 дней
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    def approve_refresh_token(self, refresh_token):
        data = jwt.decode(jwt=refresh_token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username = data.get("username")
        return self.generate_tokens(username, None, is_refresh=True)
