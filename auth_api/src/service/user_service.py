from ..db.user_repository import UserRepository
from ..entities.models import User

class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def create_user(self, name: str, email: str):
        user = User(name=name, email=email)
        self.user_repository.add_user(user)

    def get_user(self, user_id: int):
        return self.user_repository.get_user_by_id(user_id)

    def get_all_users(self):
        return self.user_repository.get_all_users()
