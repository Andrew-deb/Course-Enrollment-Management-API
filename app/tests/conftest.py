import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.schemas.user import UserCreate, UserRole
from app.schemas.course import CourseCreate
from app.service.user import UserService
from app.service.course import CourseService


@pytest.fixture(scope="function")
def client():
    return TestClient(app)

@pytest.fixture
def sample_admin_user():
    """Create and return a sample admin user"""
    user_data = UserCreate(
        name="Admin User",
        email="admin@example.com",
        role=UserRole.admin
    )
    return UserService.create_user(user_data)

@pytest.fixture(autouse=True)
def clear_db():
    """Clear in-memory database before each test"""
    from app.core.db import users, courses, enrollments
    users.clear()
    courses.clear()
    enrollments.clear()
    yield

@pytest.fixture
def sample_student_user():
    """Create and return a sample student user"""
    user_data = UserCreate(
        name="Student User",
        email="student@example.com",
        role=UserRole.student
    )
    return UserService.create_user(user_data)


@pytest.fixture
def sample_student_user2():
    """Create and return a second sample student user"""
    user_data = UserCreate(
        name="Student Two",
        email="student2@example.com",
        role=UserRole.student
    )
    return UserService.create_user(user_data)


@pytest.fixture
def sample_course():
    """Create and return a sample course"""
    course_data = CourseCreate(
        title="Introduction to Programming",
        code="CS101"
    )
    return CourseService.create_course(course_data)


@pytest.fixture
def sample_course2():
    """Create and return a second sample course"""
    course_data = CourseCreate(
        title="Data Structures",
        code="CS201"
    )
    return CourseService.create_course(course_data)