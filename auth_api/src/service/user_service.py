from ..db.user_repository import UserRepository
from src.entities.schemas import User
from src.utils.conversions import user_to_db
from passlib.context import CryptContext
from src.entities.schemas import AuthUser
from fastapi.exceptions import HTTPException
from fastapi import status
from datetime import datetime, timedelta, timezone
from src.config import SECRET_KEY, ALGORITHM
from jose import jwt, JWTError

crypt_context = CryptContext(schemes=['sha256_crypt'])


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def create_user(self, user : User):
        user.password = crypt_context.hash(user.password)
        self.user_repository.add_user(user_to_db(user))

    def get_user(self, user_id: int):
        return self.user_repository.get_user_by_id(user_id)

    def get_all_users(self):
        return self.user_repository.get_all_users()
    
    def delete_user(self, id : int):
        return self.user_repository.delete_user(id)
    
    def get_tasks_from_user(self, id : int):
        return self.user_repository.get_tasks_from_user(id)
    
    def update_user(self, user : User):
        return self.user_repository.update_user(id=user.id, name=user.name, username=user.username, password=user.password, email=user.email)
    
    def get_user_by_username(self, username : str):
        return self.user_repository.get_user_by_username(username=username)
    
    def user_login(self, user : AuthUser, expires_in : int = 30):
        try:
            user_on_db = self.user_repository.get_user_by_username(username=user.username)
        except HTTPException as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid username or password')

        if not crypt_context.verify(user.password, user_on_db.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid username or password')
        
        exp = datetime.now(timezone.utc) + timedelta(minutes=expires_in)

        payload = {
            'sub' : user.username,
            'exp' : exp
        }

        access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return {
            'access_token' : access_token,
            'exp' : exp.isoformat()
             }
    
    def verify_token(self, access_token : str):
        try:
            data = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid access token')
        
        user_on_db = self.user_repository.get_user_by_username(data['sub'])

        if not user_on_db:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid access token')
        
    def verify_token_admin(self, access_token : str):
        try:
            data = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid access token')
        
        username = data['sub']
        user_on_db = self.user_repository.get_user_by_username(username)

        if not user_on_db:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid access token')
        
        if username != 'admin':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid access token')
        
    def get_user_from_token(self, token: str):
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_username = payload.get("sub") 
        if not user_username:
            return None
        return self.get_user_by_username(user_username)
        
    def get_guilds_from_user(self, id : int):
        return self.user_repository.get_guilds_from_user(id)