from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from fastapi import Depends, HTTPException, status
from src.service.user_service import UserService

oauth_scheme = OAuth2PasswordBearer(tokenUrl='/user/login')

def token_verify(token = Depends(oauth_scheme)):
    us = UserService()
    us.verify_token(token)

def token_verify_admin(token = Depends(oauth_scheme)):
    us = UserService()
    us.verify_token_admin(token)

def get_current_user(token=Depends(oauth_scheme)):
    us = UserService()
    try:
        user = us.get_user_from_token(token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )