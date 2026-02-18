"""
Unit Tests for CourseService

Tests cover:
- create_course()
- get_course_by_id()
- get_all_courses()
- update_course()
- delete_course()

Focus on service logic, validation (duplicate codes), and CRUD operations
"""
import pytest
from app.service.course import CourseService
from app.schemas.course import CourseCreate, CourseUpdate


class TestCreateCourse:
    """Tests for CourseService.create_course() method"""
    
    def test_create_course_success(self):
        """Test creating a course with valid data"""
        course_data = CourseCreate(
            title="Introduction to Programming",
            code="CS101"
        )
        
        course = CourseService.create_course(course_data)
        
        assert course.id is not None
        assert course.title == "Introduction to Programming"
        assert course.code == "CS101"
    
    def test_create_course_auto_increment_id(self):
        """Test that course IDs are auto-incremented"""
        course_data1 = CourseCreate(title="Course One", code="CS101")
        course_data2 = CourseCreate(title="Course Two", code="CS201")
        
        course1 = CourseService.create_course(course_data1)
        course2 = CourseService.create_course(course_data2)
        
        assert course1.id == 1
        assert course2.id == 2 
    
    def test_create_course_duplicate_code_raises_error(self):
        """Test that creating a course with duplicate code raises KeyError"""
        course_data1 = CourseCreate(title="Course One", code="CS101")
        course_data2 = CourseCreate(title="Course Two", code="CS101")  # Duplicate code
        
        CourseService.create_course(course_data1)
        
        with pytest.raises(KeyError) as exc_info:
            CourseService.create_course(course_data2)
        
        assert exc_info.value.args[0] == "Course code already exists"

class TestGetCourseById:
    """Tests for CourseService.get_course_by_id() method"""
    
    def test_get_course_by_id_exists(self):
        """Test retrieving an existing course"""
        course_data = CourseCreate(title="Test Course", code="TEST101")
        created_course = CourseService.create_course(course_data)
        
        retrieved_course = CourseService.get_course_by_id(created_course.id)
        
        assert retrieved_course is not None
        assert retrieved_course.id == created_course.id
        assert retrieved_course.title == created_course.title
        assert retrieved_course.code == created_course.code
    
    def test_get_course_by_id_not_found(self):
        """Test retrieving a non-existent course returns None"""
        course = CourseService.get_course_by_id(999)
        
        assert course is None
    
    def test_get_course_by_id_correct_course(self):
        """Test that get_course_by_id returns the correct course when multiple exist"""
        course_data1 = CourseCreate(title="Course One", code="CS101")
        course_data2 = CourseCreate(title="Course Two", code="CS201")
        
        course1 = CourseService.create_course(course_data1)
        course2 = CourseService.create_course(course_data2)
        
        retrieved_course1 = CourseService.get_course_by_id(course1.id)
        retrieved_course2 = CourseService.get_course_by_id(course2.id)
        
        assert retrieved_course1.id == course1.id
        assert retrieved_course1.code == "CS101"
        assert retrieved_course2.id == course2.id
        assert retrieved_course2.code == "CS201"


class TestGetAllCourses:
    """Tests for CourseService.get_all_courses() method"""
    
    def test_get_all_courses_empty(self):
        """Test getting all courses when none exist"""
        courses = CourseService.get_all_courses()
        
        assert courses == []
        assert len(courses) == 0
    
    def test_get_all_courses(self):
        """Test getting all courses"""
        course_data1 = CourseCreate(title="Course One", code="CS101")
        course_data2 = CourseCreate(title="Course Two", code="CS201")
        course_data3 = CourseCreate(title="Course Three", code="CS301")
        
        course1 = CourseService.create_course(course_data1)
        course2 = CourseService.create_course(course_data2)
        course3 = CourseService.create_course(course_data3)
        
        courses = CourseService.get_all_courses()
        
        assert len(courses) == 3
        course_ids = [c.id for c in courses]
        assert course1.id in course_ids
        assert course2.id in course_ids
        assert course3.id in course_ids
    
    def test_get_all_courses_returns_list(self):
        """Test that get_all_courses returns a list"""
        courses = CourseService.get_all_courses()
        
        assert isinstance(courses, list)


class TestUpdateCourse:
    """Tests for CourseService.update_course() method"""
    
    def test_update_course_success(self):
        """Test updating a course successfully"""
        course_data = CourseCreate(title="Original Title", code="CS101")
        created_course = CourseService.create_course(course_data)
        
        update_data = CourseUpdate(title="Updated Title", code="CS101-NEW")
        updated_course = CourseService.update_course(created_course.id, update_data)
        
        assert updated_course.id == created_course.id
        assert updated_course.title == "Updated Title"
        assert updated_course.code == "CS101-NEW"
    
    def test_update_course_partial_title_only(self):
        """Test partial update (title only)"""
        course_data = CourseCreate(title="Original Title", code="CS101")
        created_course = CourseService.create_course(course_data)
        
        update_data = CourseUpdate(title="Updated Title")
        updated_course = CourseService.update_course(created_course.id, update_data)
        
        assert updated_course.title == "Updated Title"
        assert updated_course.code == "CS101"  # Unchanged
    
    def test_update_course_partial_code_only(self):
        """Test partial update (code only)"""
        course_data = CourseCreate(title="Original Title", code="CS101")
        created_course = CourseService.create_course(course_data)
        
        update_data = CourseUpdate(code="CS101-NEW")
        updated_course = CourseService.update_course(created_course.id, update_data)
        
        assert updated_course.title == "Original Title"  # Unchanged
        assert updated_course.code == "CS101-NEW"
    
    def test_update_course_not_found_raises_error(self):
        """Test updating non-existent course raises KeyError"""
        update_data = CourseUpdate(title="Updated Title")
        
        with pytest.raises(KeyError) as exc_info:
            CourseService.update_course(999, update_data)
        
        assert exc_info.value.args[0] == "Course not found"
    
    def test_update_course_duplicate_code_raises_error(self):
        """Test updating course with duplicate code raises KeyError"""
        course_data1 = CourseCreate(title="Course One", code="CS101")
        course_data2 = CourseCreate(title="Course Two", code="CS201")
        
        course1 = CourseService.create_course(course_data1)
        course2 = CourseService.create_course(course_data2)
        
        # Try to update course2 with course1's code
        update_data = CourseUpdate(code="CS101")
        
        with pytest.raises(KeyError) as exc_info:
            CourseService.update_course(course2.id, update_data)
        
        assert exc_info.value.args[0] == "Course with this code already exists"
    
    def test_update_course_same_code_allowed(self):
        """Test updating course keeping the same code is allowed"""
        course_data = CourseCreate(title="Original Title", code="CS101")
        created_course = CourseService.create_course(course_data)
        
        # Update with same code but different title
        update_data = CourseUpdate(title="Updated Title", code="CS101")
        updated_course = CourseService.update_course(created_course.id, update_data)
        
        assert updated_course.title == "Updated Title"
        assert updated_course.code == "CS101"


class TestDeleteCourse:
    """Tests for CourseService.delete_course() method"""
    
    def test_delete_course_success(self):
        """Test deleting a course successfully"""
        course_data = CourseCreate(title="Test Course", code="TEST101")
        created_course = CourseService.create_course(course_data)
        
        result = CourseService.delete_course(created_course.id)
        
        assert "message" in result
        assert "successfully" in result["message"].lower()
    
    def test_delete_course_not_found_raises_error(self):
        """Test deleting non-existent course raises KeyError"""
        with pytest.raises(KeyError) as exc_info:
            CourseService.delete_course(999)
        
        assert exc_info.value.args[0] == "Course not found"
