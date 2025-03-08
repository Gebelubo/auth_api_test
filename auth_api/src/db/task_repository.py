from ..db.db import Database
from sqlalchemy.orm import sessionmaker
from ..entities.models import TaskDB, UserDB
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import inspect

class TaskRepository:
    def __init__(self):
        self.db = Database()

    def add_task(self, task: TaskDB):
        session = self.db.get_session()
        user = session.query(UserDB).filter(UserDB.id == task.user_id).first()
        if not user:
            raise ValueError(f"user with id {task.user_id} not found")
        try:
            session.add(task)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_task_by_id(self, task_id: int):
        session = self.db.get_session()
        try:
            return session.query(TaskDB).filter(TaskDB.id == task_id).first()
        finally:
            session.close()

    def get_all_tasks(self):
        session = self.db.get_session()
        try:
            return session.query(TaskDB).all()
        finally:
            session.close()

    def delete_task(self, id: int):
        session = self.db.get_session()
        task = session.query(TaskDB).filter(TaskDB.id == id).first()
        if not task:
            raise ValueError(f"Task with id {id} not found")
        try:
            session.delete(task)
            session.commit()
            return task
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def update_task(self, task_id: int, **kwargs):
        session = self.db.get_session()
        task = self.get_task_by_id(task_id)

        if not task:
            raise ValueError("Task not found")

        try:
            for key, value in kwargs.items():
                if hasattr(task, key):  
                    setattr(task, key, value)
            
            session.add(task)

            state = inspect(task)
            if state.modified:
                session.commit()
                session.refresh(task)  

            return task
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()