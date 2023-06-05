import time
from datetime import datetime

from database.connection import Settings
from fastapi import HTTPException, status
from jose import jwt, JWTError
from schema.users import User

setting = Settings()

def create_access_token(user: str) -> str:
    payload ={
        "user": user,
        "expires": time.time() +3600
    }
    token = jwt.encode(payload, setting.SECRET_KEY, algorithm='HS256')
    return token

async def verify_access_token(token:str) -> dict:
    try:
        data = jwt.decode(token, setting.SECRET_KEY, algorithms=["HS256"])
        expire = data.get("expires")
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
        user_exist = await User.find_one(User.user_id == data["user"])
        print("user_exist : ", user_exist)
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