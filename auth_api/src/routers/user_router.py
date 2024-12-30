from fastapi import APIRouter, HTTPException, status, Depends
from ..service.user_service import UserService
from src.entities.schemas import User, AuthUser
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

user_service = UserService()

users_router = APIRouter(prefix='/user')

@users_router.get("/get", tags=["user"])
def list_users():
    return user_service.get_all_users()

@users_router.get("/get/id/{id}", tags=["user"])
def get_user_by_id(id : int):
    user = user_service.get_user(id)
    if not user:
        raise HTTPException(status_code=404, detail=f"user with id: {id} not found")
    return user

@users_router.post("/register", tags=["user"])
def create_user(user : User):
    user_service.create_user(user)
    return "ok"

@users_router.delete("/remove/{id}", tags=["user"])
def delete_user(id : int):
    user = user_service.delete_user(id)
    if not user:
        raise HTTPException(status_code=404, detail=f"user with id: {id} not found")
    return user

@users_router.get("/get/{id}/tasks", tags=["user"])
def get_tasks_from_user(id : int):
    return user_service.get_tasks_from_user(id)

@users_router.put("/update/{id}", tags=["user"])
def update_user(id : int, name : str, email : str):
    user_service.update_user(id, name, email)
    return "ok"

@users_router.get("/get/username/{username}", tags=["user"])
def get_user_by_username(username : str):
    return user_service.get_user_by_username(username)

@users_router.post("/login", tags=["user"])
def user_login(request_form_user : OAuth2PasswordRequestForm = Depends()):
    user = AuthUser(username=request_form_user.username, password=request_form_user.password)
    auth_data = user_service.user_login(user)
    return JSONResponse(content=auth_data, status_code=status.HTTP_200_OK)