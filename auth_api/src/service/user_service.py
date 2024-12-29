from ..db.user_repository import UserRepository
from src.entities.schemas import User
from src.utils.conversions import user_to_db

class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def create_user(self, user : User):
        self.user_repository.add_user(user_to_db(user))

    def get_user(self, user_id: int):
        return self.user_repository.get_user_by_id(user_id)

    def get_all_users(self):
        return self.user_repository.get_all_users()
    
    def delete_user(self, id : int):
        return self.user_repository.delete_user(id)
    
    def get_tasks_from_user(self, id : int):
        return self.user_repository.get_tasks_from_user(id)
    
    def update_user(self, user : User):
        return self.user_repository.update_user(id=user.id, name=user.name, username=user.username, password=user.password, email=user.email)
