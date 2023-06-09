from auth.hash_password import HashPassword
from auth.jwt_handler import create_access_token
from auth.authenticate import authenticate
from database.connection import Database
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from schema.users import User, UserUpdate, TokenResponse

from routes.train import train_manager
from routes import pubsub


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

@user_router.post("/signin", response_model=TokenResponse)
async def sign_user_in(user: OAuth2PasswordRequestForm = Depends()) -> dict:
    user_exist = await User.find_one(User.user_id == user.username)
    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with email does not exist."
        )
    if hash_password.verify_hash(user.password, user_exist.password):
        access_token = create_access_token(user_exist.user_id, is_superuser=user_exist.is_superuser)
        return {
            "access_token": access_token,
            "token_type": "Bearer",
        }

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid details passed."
    )

## admin / is_super='true'
@user_router.post("/get_user_info/") 
async def get_user_info(user: str = Depends(authenticate)) -> dict:
    if user['is_superuser']==True:
        user_info = await user_database.get_all()
        respon = {
            "state":200,
            "result":user_info,
            "message": "Success"
        }
        return respon
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid details passed."
    )

@user_router.delete("/{id}") 
async def delete_user(id, user: str = Depends(authenticate)) -> dict:
    if user['is_superuser']==True:
        try:
            await user_database.delete(id)
            user_info = await user_database.get_all()
            respon = {
                "state":200,
                "result":user_info,
                "message": "Success"
            }
            return respon
        except:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid details passed."
    )

@user_router.put("/{id}") 
async def update_auth(id, body: UserUpdate, user: str = Depends(authenticate)) -> dict:
    if user['is_superuser']==True:
        try:
            await user_database.update(id, body)
            user_info = await user_database.get_all()
            respon = {
                "state":200,
                "result":user_info,
                "message": "Success"
            }
            return respon
        except:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid details passed."
    )

@user_router.get("/get_info")
async def get_user() -> dict:
    user_info = await user_database.get_all()
    print("train_manager result :",train_manager.checking())
    await pubsub.sending_message(train_manager.checking())
    await pubsub.sending_message("test!!!")
    await pubsub.sending_message(train_manager.use_gpu())
    print("train_manager result :",train_manager.use_gpu())
    await pubsub.sending_message(train_manager.checking())
    respon = {
            "state":200,
            "result":user_info,
            "message": "Success"
        }
    return respon