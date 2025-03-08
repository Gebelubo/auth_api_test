from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()
Base.metadata.schema = "public"

class TimestampMixin:
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class GuildDB(Base, TimestampMixin):
    __tablename__ = 'guilds'
    __table_args__ = {"schema": "public"} 

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)

    guild_users = relationship('GuildUser', back_populates='guild')

    def __init__(self, name, description):
        self.name = name
        self.description = description

class UserDB(Base, TimestampMixin):
    __tablename__ = 'users'
    __table_args__ = {"schema": "public"} 

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)

    created_tasks = relationship(
        'TaskDB',
        primaryjoin="UserDB.id == TaskDB.created_by",
        foreign_keys='TaskDB.created_by',
        back_populates='creator'
    )
    assigned_tasks = relationship(
        'TaskDB',
        primaryjoin="UserDB.id == TaskDB.user_id",
        foreign_keys='TaskDB.user_id',
        back_populates='assignee'
    )

    guild_users = relationship('GuildUser', back_populates='user')

    def __init__(self, name, email, username, password):
        self.name = name
        self.username = username
        self.password = password
        self.email = email

class TaskDB(Base, TimestampMixin):
    __tablename__ = 'tasks'
    __table_args__ = {"schema": "public"} 

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    amount =  Column(Float, nullable=True)
    reward = Column(String(255), nullable=True)
    continuous = Column(Boolean, nullable=False)
    progress =  Column(Integer, nullable=True, default=0)
    limit =  Column(Integer, nullable=True, default=0)
    completed = Column(Boolean, default=False)
    created_by = Column(Integer, ForeignKey('public.users.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('public.users.id'), nullable=False)

    creator = relationship(
        'UserDB',
        primaryjoin="TaskDB.created_by == UserDB.id",
        foreign_keys=[created_by],
        back_populates='created_tasks'
    )
    assignee = relationship(
        'UserDB',
        primaryjoin="TaskDB.user_id == UserDB.id",
        foreign_keys=[user_id],
        back_populates='assigned_tasks'
    )

    def __init__(self, title, description, amount, reward, completed, continuous, progress, limit, created_by, user_id):
        self.title = title
        self.description = description
        self.amount = amount
        self.reward = reward
        self.completed = completed
        self.continuous = continuous
        self.progress = progress
        self.limit = limit
        self.created_by = created_by
        self.user_id = user_id

class GuildUser(Base, TimestampMixin): # timestamp here will be the date of entry or exit of a user
    __tablename__ = 'guild_users'

    guild_id = Column(Integer, ForeignKey('public.guilds.id', ondelete='CASCADE'), primary_key=True)
    user_id = Column(Integer, ForeignKey('public.users.id', ondelete='CASCADE'), primary_key=True)

    guild = relationship('GuildDB', back_populates='guild_users')
    user = relationship('UserDB', back_populates='guild_users')
