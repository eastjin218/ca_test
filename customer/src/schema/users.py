from beanie import Document
from typing import Optional, List
from pydantic import BaseModel, EmailStr

class User(Document):
    user_id: str
    password: str
    is_superuser : bool

    class Settings:
        name = "users"
    
    class Config:
        schema_extra = {
            "example": {
                "user_id": "smartm2m",
                "password": "strong!!!",
                "is_superuser":False
            }
        }

class UserUpdate(BaseModel):
    is_superuser: Optional[bool]

    class Config:
        schema_extra = {
            "example": {
                "is_superuser":False
            }
        }

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
