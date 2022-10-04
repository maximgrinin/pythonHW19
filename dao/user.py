# Это файл для классов доступа к данным (Data Access Object).
# Здесь должен быть класс с методами доступа к данным.
# Здесь в методах можно построить сложные запросы к БД.
from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, uid):
        return self.session.query(User).filter(User.id == uid).one()
        #return self.session.query(User).get(uid)

    def get_all(self):
        return self.session.query(User).all()

    def create(self, data):
        new_user = User(**data)
        self.session.add(new_user)
        self.session.commit()
        return new_user

    def update(self, user):
        self.session.add(user)
        self.session.commit()
        return user

    def delete(self, uid):
        user = self.get_one(uid)
        self.session.delete(user)
        self.session.commit()

    def get_by_username(self, username):
        #return self.session.query(User).filter(User.username == username).one()
        return self.session.query(User).filter(User.username == username).first()
