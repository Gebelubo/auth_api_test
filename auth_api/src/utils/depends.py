from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from src.service.user_service import UserService

oauth_scheme = OAuth2PasswordBearer(tokenUrl='/user/login')

def token_verify(token = Depends(oauth_scheme)):
    us = UserService()
    us.verify_token(token)