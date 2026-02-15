from fastapi import HTTPException,status
from app.schemas.user import UserCreate, User
from app.core.db import users

class UserService:

    # Create user
    @staticmethod
    def create_user(user_in: UserCreate):
        # Converting db object to dict
        user_dict = user_in.model_dump()

        user_id = len(users) + 1

        user = User(
            id=user_id, 
            **user_dict
        )

        users[user_id] = user

        return user

    # Retrieve user by ID
    @staticmethod
    def get_user(user_id: int):

        user = users.get(user_id)
        return user
    
    # Retrieve all users
    @staticmethod
    def get_all_users():
        return list(users.values())