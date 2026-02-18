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
    try:
        return CourseService.create_course(course_in)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@course_router.put("/{course_id}", response_model=Course, status_code=status.HTTP_200_OK)
def update_course(
    course_id: int, 
    course_in: CourseUpdate, 
    admin_user: User = Depends(is_admin_user)
    ):
    try:
        return CourseService.update_course(course_id, course_in)
    except KeyError as e:
        error_msg = str(e.args[0])
        if "Course not found" in error_msg:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_msg)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_msg)

@course_router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(
    course_id: int, 
    admin_user: User = Depends(is_admin_user)
    ):
    try:
        CourseService.delete_course(course_id)
        return None
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

# Public endpoints
@course_router.get("/{course_id}", response_model=Course)
def get_course_by_id(course_id: int):
    course = CourseService.get_course_by_id(course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return course

@course_router.get("/", response_model=List[Course])
def get_all_courses():
    return CourseService.get_all_courses()
