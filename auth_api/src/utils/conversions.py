from src.entities.models import UserDB, TaskDB
from src.entities.schemas import User, Task

def user_from_db(user : UserDB):
    return User.model_validate(user)

def user_to_db(user : User):
    return UserDB(name=user.name, email=user.email, username=user.username, password=user.password)

def task_from_db(task : TaskDB):
    return Task.model_validate(task)

def task_to_db(task : Task):
    return TaskDB(title=task.title, description=task.description, amount=task.amount, reward=task.reward, completed=False, user_id=task.user_id)