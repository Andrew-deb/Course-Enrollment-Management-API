from fastapi import APIRouter, HTTPException, status
from app.schemas.user import UserCreate
from app.service.user import UserService


user_router = APIRouter()


# Admin-only endpoint
@user_router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate):
    return UserService.create_user(user_data)

@user_router.get("/{user_id}")
def get_user(user_id: int):
    
    user = UserService.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user