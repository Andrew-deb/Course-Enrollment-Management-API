from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from app.schemas.enrollment import Enrollment, EnrollmentCreate
from app.schemas.user import User
from app.service.enrollment import EnrollmentService
from app.service.course import CourseService
from app.api.deps import is_student_user, is_admin_user

enrollment_router = APIRouter(tags=["Enrollments"])

# Student-only endpoint
# Enroll in a course
@enrollment_router.post("/", response_model=Enrollment, status_code=status.HTTP_201_CREATED)
def create_enrollment(
    enrollment_in: EnrollmentCreate, 
    user: User = Depends(is_student_user)
    ):
    return EnrollmentService.create_enrollment(enrollment_in)

# Deregister from a course
@enrollment_router.delete("/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
def deregister_enrollment(
    enrollment_id: int, 
    user: User = Depends(is_student_user)
    ):
    return EnrollmentService.delete_enrollment(enrollment_id)
   

# Retrieve enrollments for a specific student
@enrollment_router.get("/my-enrollments", response_model=List[Enrollment])
def get_my_enrollments(user: User = Depends(is_student_user)):
    return EnrollmentService.get_enrollments_by_user(user.id)

# Admin-only endpoint
# Retrieve all enrollments

@enrollment_router.get("/", response_model=List[Enrollment])
def get_all_enrollments(admin_user: User = Depends(is_admin_user)):
    return EnrollmentService.get_all_enrollments()

# Retrieve Enrollment for a specific course

@enrollment_router.get("/course/{course_id}", response_model=List[Enrollment])
def get_enrollments_by_course(
    course_id: int, admin_user: User = Depends(is_admin_user)
    ):
    course = CourseService.get_course_by_id(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return EnrollmentService.get_enrollments_by_course(course_id)

# Force deregister a student from a course 
@enrollment_router.delete("/force/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
def force_deregister_enrollment(
    enrollment_id: int, 
    admin_user: User = Depends(is_admin_user)
    ):
    return EnrollmentService.delete_enrollment(enrollment_id)
    