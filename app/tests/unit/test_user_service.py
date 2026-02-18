"""
Unit Tests for UserService

Tests cover:
- create_user()
- get_user()
- get_all_users()

Focus on service logic, ID generation, and data storage
"""
import pytest
from app.service.user import UserService
from app.schemas.user import UserCreate, UserRole


class TestCreateUser:
    """Tests for UserService.create_user() method"""
    
    def test_create_user_auto_increment_id(self):
        """Test that user IDs are auto-incremented"""
        user_data1 = UserCreate(
            name="User One",
            email="user1@example.com",
            role=UserRole.student
        )
        user_data2 = UserCreate(
            name="User Two",
            email="user2@example.com",
            role=UserRole.admin
        )
        
        user1 = UserService.create_user(user_data1)
        user2 = UserService.create_user(user_data2)
        
        assert user1.id == 1
        assert user2.id == 2
    
    def test_create_admin_user(self):
        """Test creating an admin user"""
        user_data = UserCreate(
            name="Admin User",
            email="admin@example.com",
            role=UserRole.admin
        )
        
        user = UserService.create_user(user_data)
        
        assert user.role == UserRole.admin
    
    def test_create_student_user(self):
        """Test creating a student user"""
        user_data = UserCreate(
            name="Student User",
            email="student@example.com",
            role=UserRole.student
        )
        
        user = UserService.create_user(user_data)
        
        assert user.role == UserRole.student


class TestGetUser:
    """Tests for UserService.get_user() method"""
    
    def test_get_user_exists(self):
        """Test retrieving an existing user"""
        # Create a user first
        user_data = UserCreate(
            name="Test User",
            email="test@example.com",
            role=UserRole.student
        )
        created_user = UserService.create_user(user_data)
        
        # Retrieve the user
        retrieved_user = UserService.get_user(created_user.id)
        
        assert retrieved_user is not None
        assert retrieved_user.id == created_user.id
        assert retrieved_user.name == created_user.name
        assert retrieved_user.email == created_user.email
        assert retrieved_user.role == created_user.role
    
    def test_get_user_not_found(self):
        """Test retrieving a non-existent user returns None"""
        user = UserService.get_user(999)
        
        assert user is None


class TestGetAllUsers:
    """Tests for UserService.get_all_users() method"""
    
    def test_get_all_users_empty(self):
        """Test getting all users when none exist"""
        users = UserService.get_all_users()
        
        assert users == []
        assert len(users) == 0

    def test_get_all_users_when_users_exist(self):
        """Test getting all users when some users exist"""
        # Create some users first
        user_data1 = UserCreate(
            name="User One",
            email="user1@example.com",
            role=UserRole.student
        )
        user_data2 = UserCreate(
            name="User Two",
            email="user2@example.com",
            role=UserRole.admin
        )
        
        UserService.create_user(user_data1)
        UserService.create_user(user_data2)
        
        users = UserService.get_all_users()
        
        assert len(users) == 2
        user_names = [u.name for u in users]
        assert "User One" in user_names
        assert "User Two" in user_names

    def test_get_all_users_returns_list(self):
        """Test that get_all_users returns a list"""
        users = UserService.get_all_users()
        
        assert isinstance(users, list)
