from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
Base.metadata.schema = "public"

class User(Base):
    __tablename__ = 'users'
    __table_args__ = {"schema": "public"} 

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)

    tasks = relationship("Task", back_populates="user")

    def __init__(self, name, email):
        self.name = name
        self.email = email

class Task(Base):
    __tablename__ = 'tasks'
    __table_args__ = {"schema": "public"} 

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    amount =  Column(Float, nullable=True)
    reward = Column(String(255), nullable=True)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship("User", back_populates="tasks")

    def __init__(self, title, description, amount, reward, user_id):
        self.title = title
        self.description = description
        self.amount = amount
        self.reward = reward
        self.user_id = user_id
