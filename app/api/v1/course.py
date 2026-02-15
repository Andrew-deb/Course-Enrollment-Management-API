from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from app.schemas.course import Course, CourseCreate, CourseUpdate
from app.schemas.user import User
from app.service.course import CourseService
from app.api.deps import is_admin_user

course_router = APIRouter()

# Admin-only endpoint

@course_router.post("/", response_model=Course, status_code=status.HTTP_201_CREATED)
def create_course(
    course_in: CourseCreate, 
    admin_user: User = Depends(is_admin_user)
    ):
    return CourseService.create_course(course_in)

@course_router.put("/{course_id}", response_model=Course, status_code=status.HTTP_200_OK)
def update_course(
    course_id: int, 
    course_in: CourseUpdate, 
    admin_user: User = Depends(is_admin_user)
    ):
    return CourseService.update_course(course_id, course_in)

@course_router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(
    course_id: int, 
    admin_user: User = Depends(is_admin_user)
    ):
    CourseService.delete_course(course_id)
    return None

# Public endpoints
@course_router.get("/{course_id}", response_model=Course)
def get_course_by_id(course_id: int):
    course = CourseService.get_course_by_id(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@course_router.get("/", response_model=List[Course])
def get_all_courses():
    return CourseService.get_all_courses()
