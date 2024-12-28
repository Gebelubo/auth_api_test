from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.routers.user_router import users_router
from src.routers.task_router import tasks_router
from src.db.db import Database

db = Database()

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    print("ok")
    db.test_connection()
    db.create_tables()


app.include_router(users_router)
app.include_router(tasks_router)

