from auth.hash_password import HashPassword
from database.connection import Database
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from schema.users import User, TokenResponse

user_router = APIRouter(
    tags=["User"],
)

user_database = Database(User)
hash_password = HashPassword()

@user_router.post("/signup")
async def sign_user_up(user: User) -> dict:
    user_exist = await User.find_one(User.user_id == user.user_id)

    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with ID provided exists already."
        )
    hashed_password = hash_password.create_hash(user.password)
    user.password = hashed_password
    await user_database.save(user)
    return {
        "message": "User created successfully"
    }

@user_router.get("/get_info")
async def get_user_info() -> dict:
    user_info = await user_database.get_all()
    return {"message" : user_info}