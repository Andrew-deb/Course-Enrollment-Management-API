from app.schemas.course import CourseCreate, CourseUpdate, Course
from app.core.db import courses

class CourseService:
    # Create course
    @staticmethod
    def create_course(course_in: CourseCreate):
        course_dict = course_in.model_dump()

        #To check if course code already exists
        for course in courses.values():
            if course.code == course_dict['code']:
                raise KeyError("Course code already exists")

        course_id = len(courses) + 1

        new_course = Course(
            id=course_id,
            **course_dict
        )

        courses[course_id] = new_course

        return new_course

    # Retrieve course by ID
    @staticmethod
    def get_course_by_id(course_id: int):
        course = courses.get(course_id)
        return course
    
    # Retrieve all courses
    @staticmethod
    def get_all_courses():
        return list(courses.values())
    
    # Update course
    @staticmethod
    def update_course(course_id: int, course_in: CourseUpdate):
        course = courses.get(course_id)
        if not course:
            raise KeyError("Course not found")

        update_data = course_in.model_dump(exclude_unset=True)

        # Check unique code if updating
        if 'code' in update_data:
            for c in courses.values():
                if c.code == update_data['code'] and c.id != course_id:
                    raise KeyError("Course code already exists")

        updated_course = course.model_copy(update=update_data)

        courses[course_id] = updated_course

        return updated_course
    
    # Delete course
    @staticmethod
    def delete_course(course_id: int):

        if course_id not in courses:
            raise KeyError("Course not found")

        del courses[course_id]

        return {"message": "Course deleted successfully"}

