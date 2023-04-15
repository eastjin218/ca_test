import time
from datetime import datetime

from database.connection import Settings
from fastapi import HTTPException, status
from jose import jwt, JWTError
from schemes.users import User

setting = Settings()

def create_access_token(user: str) -> str:
    payload ={
        "user": user,
        "expires": time.time() +3600
    }
    token = jwt.encode(pyload, settings.SECRET_KEY, algorithm='HS256')
    return token

async def verify_access_token(token:str) -> dict:
    try:
        data = jwt.decode(token, settings.SECRET_KEY, algorithm=["HS256"])
        
        expire = data.get("expoires")
        if expire is None:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail="No access token supplied"
            )
        if datetime.utcnow() > datetime.utcfromtimestamp(expire):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail = "Token expired!"
            )
        user_exist = await User.find_one(User.email == data["User"])
        if not user_exist:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail = "Invalid token"
            )
            
        return data
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token"
        )