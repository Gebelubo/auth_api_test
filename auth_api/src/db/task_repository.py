from ..db.db import Database
from sqlalchemy.orm import sessionmaker
from ..entities.models import TaskDB, UserDB

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
        except Exception as e:
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

    def delete_task(self, id : int):
        task = self.get_task_by_id(id)
        session = self.db.get_session()
        try:
            session.delete(task)
            session.commit()
            return task
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

