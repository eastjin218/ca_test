from beanie import Document

from pydantic import BaseModel, EmailStr

class User(Document):
    user_id: str
    password: str

    class Settings:
        name = "users"
    
    class Config:
        schema_extra = {
            "example": {
                "user_id": "smartm2m",
                "password": "strong!!!"
            }
        }

class TokenResponse(BaseModel):
    access_token: str
    token_type: str