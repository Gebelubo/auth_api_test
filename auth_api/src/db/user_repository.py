from ..db.db import Database
from sqlalchemy.orm import sessionmaker
from ..entities.models import User, Task

class UserRepository:
    def __init__(self):
        self.db = Database()

    def add_user(self, user: User):
        session = self.db.get_session()
        try:
            session.add(user)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_user_by_id(self, user_id: int):
        session = self.db.get_session()
        try:
            return session.query(User).filter(User.id == user_id).first()
        finally:
            session.close()

    def get_all_users(self):
        session = self.db.get_session()
        try:
            return session.query(User).all()
        finally:
            session.close()

    def delete_user(self, id : int):
        user = self.get_user_by_id(id)
        session = self.db.get_session()
        try:
            session.delete(user)
            session.commit()
            return user
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_tasks_from_user(self, id : int):
        session = self.db.get_session()
        tasks = session.query(Task).filter(Task.user_id == id).all()
        return tasks

