from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    name : str
    username : str
    password : str
    email : str

    model_config = ConfigDict(from_attributes=True)

class Task(BaseModel):
    title : str
    description : str
    amount : float
    reward : str
    user_id : int

    model_config = ConfigDict(from_attributes=True)
