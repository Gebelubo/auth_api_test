from ..db.db import Database
from sqlalchemy.orm import sessionmaker
from ..entities.models import GuildDB, UserDB, GuildUser
from sqlalchemy.orm import joinedload
from ..utils.conversions import userdb_to_dto

class GuildRepository:
    def __init__(self):
        self.db = Database()

    def add_guild(self, guild: GuildDB):
        session = self.db.get_session()
        try:
            session.add(guild)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_guild_by_id(self, guild_id: int):
        session = self.db.get_session()
        try:
            return session.query(GuildDB).filter(GuildDB.id == guild_id).first()
        finally:
            session.close()

    def get_all_guilds(self):
        session = self.db.get_session()
        try:
            return session.query(GuildDB).all()
        finally:
            session.close()

    def delete_guild(self, id : int):
        guild = self.get_guild_by_id(id)
        session = self.db.get_session()
        try:
            session.delete(guild)
            session.commit()
            return guild
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_guild_users(self, id : int):
        try:
            session = self.db.get_session()
            guild = session.query(GuildDB).options(joinedload(GuildDB.guild_users)).filter(GuildDB.id == id).first()
            if guild:
                return [userdb_to_dto(guild_user.user) for guild_user in guild.guild_users]
            return []
        finally:
            session.close()
    
    def add_user_to_guild(self, guild_id: int, user_id: int):
        session = self.db.get_session()
        try:
            guild = session.query(GuildDB).filter(GuildDB.id == guild_id).first()
            user = session.query(UserDB).filter(UserDB.id == user_id).first()

            if not guild:
                raise ValueError(f"Guild with id {guild_id} not found.")
            if not user:
                raise ValueError(f"User with id {user_id} not found")

            existing_relation = (
                session.query(GuildUser)
                .filter(GuildUser.guild_id == guild_id, GuildUser.user_id == user_id)
                .first()
            )
            if existing_relation:
                raise ValueError(f"User with id {user_id} already in the guild {guild_id}.")

            guild_user = GuildUser(guild_id=guild_id, user_id=user_id)
            session.add(guild_user)
            session.commit()
            return guild_user
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()


