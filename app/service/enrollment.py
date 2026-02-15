from fastapi import HTTPException, status
from app.schemas.enrollment import EnrollmentCreate, Enrollment
from app.core.db import enrollments, users, courses

class EnrollmentService:

    # Create enrollment
    @staticmethod
    def create_enrollment(enrollment_in: EnrollmentCreate):

        # Check user exists
        user = users.get(enrollment_in.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )

        # Check course exists
        course = courses.get(enrollment_in.course_id)
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found."
            )

        # Check duplicate enrollment
        for enrollment in enrollments.values():
            if (
                enrollment.user_id == enrollment_in.user_id and
                enrollment.course_id == enrollment_in.course_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Student already enrolled in this course."
                )

        enrollment_dict = enrollment_in.model_dump()

        enrollment_id = len(enrollments) + 1

        new_enrollment = Enrollment(
            id=enrollment_id,
            **enrollment_dict
        )

        enrollments[enrollment_id] = new_enrollment

        return new_enrollment
    
    # Get all enrollments
    @staticmethod
    def get_all_enrollments():
        return list(enrollments.values())
    

    # Get enrollment for a specific student
    @staticmethod
    def get_enrollments_by_user(user_id: int):

        for enrollment in enrollments.values():
            if enrollment.user_id == user_id:
                return enrollment
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found for this user."
        )

    # Get enrollment for a specific course
    @staticmethod
    def get_enrollments_by_course(course_id: int):

        for enrollment in enrollments.values():
            if enrollment.course_id == course_id:
                return enrollment
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found for this course."
        )
    
    # Delete enrollment
    @staticmethod
    def delete_enrollment(enrollment_id: int):

        if enrollment_id not in enrollments:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Enrollment not found."
            )

        del enrollments[enrollment_id]

        return {"detail": "Enrollment deleted successfully."}
