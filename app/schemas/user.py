from pydantic import BaseModel, EmailStr, Field
from enum import Enum

class UserRole(str, Enum):
    student = "student"
    admin = "admin"


class UserBase(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    role: UserRole

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
