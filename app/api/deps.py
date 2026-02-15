from fastapi import HTTPException, status
from app.schemas.user import UserCreate, User, UserRole
from app.service.user import UserService

# Since we didn't handle "user not found" in the get_user function in the service layer.
def get_user(user_id: int):
    user = UserService.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

def is_admin_user(user_id: int):
    user = get_user(user_id)
    
    if user.role != User.Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Admin privileges required"
            )
    return user
    
def is_student_user(user_id: int):
    user = get_user(user_id)

    if user.role != UserRole.STUDENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can perform this action."
        )

    return user
    