from fastapi import APIRouter
from ..service.user_service import UserService
from src.db.db import Database

user_service = UserService()

users_router = APIRouter()

@users_router.get("/user", tags=" User")
def list_users():
    return user_service.get_all_users()

@users_router.post("/user", tags=" User")
def create_user(name: str, email : str):
    user_service.create_user(name=name, email=email)
