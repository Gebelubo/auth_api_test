from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
import re
import datetime

class User(BaseModel):
    name : str
    username : str
    password : str
    email : str

    model_config = ConfigDict(from_attributes=True)

    @field_validator('email')
    def validate_email(cls, value):
        pattern = r'^[a-zA-Z0-9_]+@[a-zA-Z0-9_]+\.[a-zA-Z]+$'
        if not re.match(pattern, value):
            raise ValueError('email format invalid')
        return value



class Task(BaseModel):
    title: str
    description: str
    amount: float
    reward: str
    continuous: bool = False
    limit: Optional[int]
    user_id: int
    model_config = ConfigDict(from_attributes=True)

class Guild(BaseModel):
    name : str
    description: str


class AuthUser(BaseModel):
    username: str
    password : str

    @field_validator("username")
    def validate_username(cls, value):
        pattern = r'^[a-z0-9_]+$'
        if not re.match(pattern, value):
            raise ValueError('Username format invalid')
        return value
