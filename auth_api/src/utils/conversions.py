from src.entities.models import UserDB, TaskDB, GuildDB
from src.entities.schemas import User, Task, Guild
from src.entities.DTO import UserDTO

def user_from_db(user : UserDB):
    return User.model_validate(user)

def user_to_db(user : User):
    return UserDB(name=user.name, email=user.email, username=user.username, password=user.password)

def userdb_to_dto(user : UserDB):
    return UserDTO(id=user.id, username=user.username, email=user.email)

def task_from_db(task : TaskDB):
    return Task.model_validate(task)

def task_to_db(task : Task, id : int):
    return TaskDB(title=task.title, description=task.description, amount=task.amount, reward=task.reward, completed=False, continuous=task.continuous, progress=0, limit=task.limit, created_by=id, user_id=task.user_id)

def guild_to_db(guild : Guild):
    return GuildDB(name=guild.name, description=guild.description)