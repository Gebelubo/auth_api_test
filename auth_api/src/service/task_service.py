from ..db.task_repository import TaskRepository
from src.entities.schemas import Task
from src.utils.conversions import task_to_db

class TaskService:
    def __init__(self):
        self.task_repository = TaskRepository()

    def create_task(self, task : Task, user):
        id = user.id
        self.task_repository.add_task(task_to_db(task, id=id))

    def get_task(self, task_id: int):
        return self.task_repository.get_task_by_id(task_id)

    def get_all_tasks(self):
        return self.task_repository.get_all_tasks()
    
    def delete_task(self, task_id : int):
        return self.task_repository.delete_task(task_id)
    
    def add_one_progress(self, task_id:int):
        task = self.task_repository.get_task_by_id(task_id)
        if not task.completed:
            progress = task.progress + 1
            limit = task.limit
            if (progress>=limit) and (limit>0):
                self.task_repository.update_task(task_id=task_id, completed=True)
                return "task completed"
            else:
                return self.task_repository.update_task(task_id=task_id, progress=progress)
        return "task already done"
