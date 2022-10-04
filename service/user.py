# Здесь бизнес логика, в виде классов или методов.
# Сюда импортируются DAO классы из пакета dao и модели из dao.model
# Некоторые методы могут оказаться просто прослойкой между dao и views,
# но чаще всего будет какая-то логика обработки данных сейчас или в будущем.
from dao.user import UserDAO

import base64
import hashlib
import hmac
from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS, PWD_HASH_ALGORITHM


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_all(self):
        return self.dao.get_all()

    def create(self, data):
        # Тут вся логика криэйта
        # Шифруем пароль
        data['password'] = self.get_hash(data.get('password'))
        return self.dao.create(data)

    def update(self, uid, data):
        # Тут вся логика апдейта
        user = self.get_one(uid)
        [setattr(user, key, value) for key, value in data.items()]
        self.dao.update(user)
        return self.dao

    def delete(self, uid):
        self.dao.delete(uid)

    def get_by_username(self, username):
        return self.dao.get_by_username(username)

    def get_hash(self, password):
        hash_digest = hashlib.pbkdf2_hmac(
            PWD_HASH_ALGORITHM,
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )
        return base64.b64encode(hash_digest)

    def compare_passwords(self, hash_password, clear_password) -> bool:
        decoded_digest = base64.b64decode(hash_password)
        hash_digest = base64.b64decode(self.get_hash(clear_password))
        return hmac.compare_digest(decoded_digest, hash_digest)
