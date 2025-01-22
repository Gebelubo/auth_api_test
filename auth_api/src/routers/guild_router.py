from fastapi import APIRouter, HTTPException
from ..service.guild_service import GuildService
from ..entities.schemas import Guild

guild_service = GuildService()

guild_router = APIRouter(prefix='/guild')

@guild_router.get("/get", tags=['guild'])
def list_guilds():
    return guild_service.get_all_guilds()

@guild_router.get("/get/{id}/users", tags=['guild'])
def list_members(id : int):
    return guild_service.get_guild_members(id)

@guild_router.get("/get/id/{id}", tags=['guild'])
def get_guild_by_id(id : int):
    return guild_service.get_guild_by_id(id)

@guild_router.post("/create", tags=['guild'])
def create_guild(guild : Guild):
    try:
        guild_service.create_guild(guild)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=ve.args[0])
    return "ok"

@guild_router.post("/insert/user/{user_id}", tags=['guild'])
def insert_member(guild_id : int, user_id : int):
    try:
        guild_service.insert_member(guild_id=guild_id, user_id=user_id)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=ve.args[0])
    return "ok"
