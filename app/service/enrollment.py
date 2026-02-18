from typing import List
from app.schemas.enrollment import EnrollmentCreate, Enrollment
from app.core.db import enrollments, users, courses

class EnrollmentService:

    # Create enrollment
    @staticmethod
    def create_enrollment(enrollment_in: EnrollmentCreate):

        # Check user exists
        user = users.get(enrollment_in.user_id)
        if not user:
            raise KeyError("User not found")

        # Check course exists
        course = courses.get(enrollment_in.course_id)
        if not course:
            raise KeyError("Course not found")

        # Check duplicate enrollment
        for enrollment in enrollments.values():
            if (
                enrollment.user_id == enrollment_in.user_id and
                enrollment.course_id == enrollment_in.course_id
            ):
                raise ValueError("User is already enrolled in this course")

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

        enrollments_for_user = []
        for enrollment in enrollments.values():
            if enrollment.user_id == user_id:
                enrollments_for_user.append(enrollment)
        return enrollments_for_user

    # Get enrollment for a specific course
    @staticmethod
    def get_enrollments_by_course(course_id: int):

        enrollments_for_course = []

        for enrollment in enrollments.values():
            if enrollment.course_id == course_id:
                enrollments_for_course.append(enrollment)

        return enrollments_for_course
    
    # Delete enrollment
    @staticmethod
    def delete_enrollment(enrollment_id: int):

        if enrollment_id not in enrollments:
            raise KeyError("Enrollment not found")

        del enrollments[enrollment_id]

        return {"detail": "Enrollment deleted successfully."}
