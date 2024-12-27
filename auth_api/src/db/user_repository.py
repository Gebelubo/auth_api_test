from ..db.db import Database
from sqlalchemy.orm import sessionmaker
from ..entities.models import User

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
