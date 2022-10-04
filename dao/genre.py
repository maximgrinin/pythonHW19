# Это файл для классов доступа к данным (Data Access Object).
# Здесь должен быть класс с методами доступа к данным
# Здесь в методах можно построить сложные запросы к БД
from dao.model.genre import Genre


class GenreDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, gid):
        return self.session.query(Genre).filter(Genre.id == gid).one()

    def get_all(self):
        return self.session.query(Genre).all()

    def create(self, data):
        new_genre = Genre(**data)
        self.session.add(new_genre)
        self.session.commit()
        return new_genre

    def update(self, genre):
        self.session.add(genre)
        self.session.commit()
        return genre

    def delete(self, gid):
        genre = self.get_one(gid)
        self.session.delete(genre)
        self.session.commit()
