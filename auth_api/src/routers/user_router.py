from fastapi import APIRouter, HTTPException
from ..service.user_service import UserService
from src.entities.schemas import User

user_service = UserService()

users_router = APIRouter()

@users_router.get("/user", tags=["user"])
def list_users():
    return user_service.get_all_users()

@users_router.get("/user/{id}", tags=["user"])
def get_user_by_id(id : int):
    user = user_service.get_user(id)
    if not user:
        raise HTTPException(status_code=404, detail=f"user with id: {id} not found")
    return user

@users_router.post("/user", tags=["user"])
def create_user(user : User):
    user_service.create_user(user)
    return "ok"

@users_router.delete("/user/{id}", tags=["user"])
def delete_user(id : int):
    user = user_service.delete_user(id)
    if not user:
        raise HTTPException(status_code=404, detail=f"user with id: {id} not found")
    return user

@users_router.get("/user/{id}/tasks", tags=["user"])
def get_tasks_from_user(id : int):
    return user_service.get_tasks_from_user(id)

@users_router.put("/user/{id}", tags=["user"])
def update_user(id : int, name : str, email : str):
    user_service.update_user(id, name, email)
    return "ok"
