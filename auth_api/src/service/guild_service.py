from ..db.guild_repository import GuildRepository
from ..utils.conversions import guild_to_db
from ..entities.schemas import Guild

class GuildService:
    def __init__(self):
        self.guild_repository = GuildRepository()

    def create_guild(self, guild : Guild):
        self.guild_repository.add_guild(guild_to_db(guild))

    def get_all_guilds(self):
        return self.guild_repository.get_all_guilds()
    
    def get_guild_members(self, guild_id : int):
        return self.guild_repository.get_guild_users(guild_id)
    
    def get_guild_by_id(self, id : int):
        return self.guild_repository.get_guild_by_id(id)
    
    def insert_member(self, guild_id : int, user_id : int):
        self.guild_repository.add_user_to_guild(guild_id=guild_id, user_id=user_id)