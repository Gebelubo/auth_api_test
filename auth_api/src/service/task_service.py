from ..db.task_repository import TaskRepository
from src.entities.schemas import Task
from src.utils.conversions import task_to_db

class TaskService:
    def __init__(self):
        self.task_repository = TaskRepository()

    def create_task(self, task : Task):
        self.task_repository.add_task(task_to_db(task))

    def get_task(self, task_id: int):
        return self.task_repository.get_task_by_id(task_id)

    def get_all_tasks(self):
        return self.task_repository.get_all_tasks()
    
    def delete_task(self, id : int):
        return self.task_repository.delete_task(id)
