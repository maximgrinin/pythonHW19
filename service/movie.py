# Здесь бизнес логика, в виде классов или методов.
# Сюда импортируются DAO классы из пакета dao и модели из dao.model
# Некоторые методы могут оказаться просто прослойкой между dao и views,
# но чаще всего будет какая-то логика обработки данных сейчас или в будущем.
from dao.movie import MovieDAO


class MovieService:
    def __init__(self, dao: MovieDAO):
        self.dao = dao

    def get_one(self, mid):
        return self.dao.get_one(mid)

    def get_all(self, args=None):
        return self.dao.get_all(args)

    def create(self, data):
        return self.dao.create(data)

    def update(self, mid, data):
        # Тут вся логика апдейта
        movie = self.get_one(mid)
        [setattr(movie, key, value) for key, value in data.items()]
        self.dao.update(movie)
        return self.dao

    def delete(self, mid):
        self.dao.delete(mid)
