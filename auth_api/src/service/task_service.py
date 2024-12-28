from ..db.task_repository import TaskRepository
from ..entities.models import Task

class TaskService:
    def __init__(self):
        self.task_repository = TaskRepository()

    def create_task(self, title: str, description: str, amount : float, reward : str, user_id : int):
        task = Task(title=title, description=description, amount=amount, reward=reward, user_id=user_id)
        self.task_repository.add_task(task)

    def add_task(self, task : Task):
        self.task_repository.add_task(task)

    def get_task(self, task_id: int):
        return self.task_repository.get_task_by_id(task_id)

    def get_all_tasks(self):
        return self.task_repository.get_all_tasks()
    
    def delete_task(self, id : int):
        return self.task_repository.delete_task(id)
