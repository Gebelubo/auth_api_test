from ..db.db import Database
from sqlalchemy.orm import sessionmaker
from ..entities.models import UserDB, TaskDB, GuildDB
from fastapi.exceptions import HTTPException
from fastapi import status

class UserRepository:
    def __init__(self):
        self.db = Database()

    def add_user(self, user: UserDB):
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
            user = session.query(UserDB).filter(UserDB.id == user_id).first()
            if not user:
                raise ValueError(f"User with id: {user_id} not found")
        finally:
            session.close()
        return user

    def get_all_users(self):
        session = self.db.get_session()
        try:
            return session.query(UserDB).all()
        finally:
            session.close()

    def delete_user(self, id : int):
        user = self.get_user_by_id(id)
        session = self.db.get_session()
        try:
            session.query(TaskDB).filter(TaskDB.user_id == id).delete()
            session.delete(user)
            session.commit()
            return user
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_tasks_from_user(self, id : int):
        try:
            session = self.db.get_session()
            tasks = session.query(TaskDB).filter(TaskDB.user_id == id).all()
        finally:
            session.close()
        return tasks
    
    def get_guilds_from_user(self, id : int):
        try:
            session = self.db.get_session()
            guilds = session.query(GuildDB).filter(GuildDB.user_id == id).all()
        finally:
            session.close()
        return guilds

    def update_user(self, id : int, name : str, username : str, password : str, email : str):
        try:
            session = self.db.get_session()
            rows_updated = session.query(UserDB).filter_by(id=id).update(
                {"name": name, "username" : username, "password" : password, "email": email},
                synchronize_session=False
            )
            if rows_updated == 0:
                raise ValueError(f"User with id {id} not found.")
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_user_by_username(self, username : str):
        session = self.db.get_session()
        user = session.query(UserDB).filter(UserDB.username == username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with username {username} not found')
        return user



    

