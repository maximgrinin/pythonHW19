# Здесь бизнес логика, в виде классов или методов.
# Сюда импортируются DAO классы из пакета dao и модели из dao.model
# Некоторые методы могут оказаться просто прослойкой между dao и views,
# но чаще всего будет какая-то логика обработки данных сейчас или в будущем.
from dao.genre import GenreDAO


class GenreService:
    def __init__(self, dao: GenreDAO):
        self.dao = dao

    def get_one(self, gid):
        return self.dao.get_one(gid)

    def get_all(self):
        return self.dao.get_all()

    def create(self, data):
        return self.dao.create(data)

    def update(self, gid, data):
        # Тут вся логика апдейта
        genre = self.get_one(gid)
        [setattr(genre, key, value) for key, value in data.items()]
        self.dao.update(genre)
        return self.dao

    def delete(self, gid):
        self.dao.delete(gid)
