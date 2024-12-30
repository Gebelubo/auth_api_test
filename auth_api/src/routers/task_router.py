from fastapi import APIRouter, HTTPException
from ..service.task_service import TaskService
from src.entities.schemas import Task

task_service = TaskService()

tasks_router = APIRouter(prefix='/task')

@tasks_router.get("/get", tags=["task"])
def list_tasks():
    return task_service.get_all_tasks()

@tasks_router.get("/get/{id}", tags=["task"])
def get_task_by_id(id : int):
    task = task_service.get_task(id)
    if not task:
        raise HTTPException(status_code=404, detail=f"task with id: {id} not found")
    return task

@tasks_router.post("/register", tags=["task"])
def create_task(task : Task):
    try:
        task_service.create_task(task)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=ve.args[0])
    return "ok"

@tasks_router.delete("/remove/{id}", tags=["task"])
def delete_task(id : int):
    task = task_service.delete_task(id)
    if not task:
        raise HTTPException(status_code=404, detail=f"task with id: {id} not found")
    return task

