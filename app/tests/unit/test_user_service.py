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
    
    def test_create_user_success(self):
        """Test creating a user with valid data"""
        user_data = UserCreate(
            name="John Doe",
            email="john@example.com",
            role=UserRole.student
        )
        
        user = UserService.create_user(user_data)
        
        assert user.id is not None
        assert user.name == "John Doe"
        assert user.email == "john@example.com"
        assert user.role == UserRole.student
    
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
    
    def test_create_user_stored_correctly(self):
        """Test that created user is stored in database"""
        user_data = UserCreate(
            name="Test User",
            email="test@example.com",
            role=UserRole.student
        )
        
        created_user = UserService.create_user(user_data)
        retrieved_user = UserService.get_user(created_user.id)
        
        assert retrieved_user is not None
        assert retrieved_user.id == created_user.id
        assert retrieved_user.name == created_user.name


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
    
    def test_get_user_correct_user(self):
        """Test that get_user returns the correct user when multiple exist"""
        user_data1 = UserCreate(name="User One", email="user1@example.com", role=UserRole.student)
        user_data2 = UserCreate(name="User Two", email="user2@example.com", role=UserRole.admin)
        
        user1 = UserService.create_user(user_data1)
        user2 = UserService.create_user(user_data2)
        
        retrieved_user1 = UserService.get_user(user1.id)
        retrieved_user2 = UserService.get_user(user2.id)
        
        assert retrieved_user1.id == user1.id
        assert retrieved_user1.name == "User One"
        assert retrieved_user2.id == user2.id
        assert retrieved_user2.name == "User Two"


class TestGetAllUsers:
    """Tests for UserService.get_all_users() method"""
    
    def test_get_all_users_empty(self):
        """Test getting all users when none exist"""
        users = UserService.get_all_users()
        
        assert users == []
        assert len(users) == 0
    
    def test_get_all_users_single(self):
        """Test getting all users when one exists"""
        user_data = UserCreate(
            name="Test User",
            email="test@example.com",
            role=UserRole.student
        )
        created_user = UserService.create_user(user_data)
        
        users = UserService.get_all_users()
        
        assert len(users) == 1
        assert users[0].id == created_user.id
        assert users[0].name == created_user.name
    
    def test_get_all_users_multiple(self):
        """Test getting all users when multiple exist"""
        user_data1 = UserCreate(name="User One", email="user1@example.com", role=UserRole.student)
        user_data2 = UserCreate(name="User Two", email="user2@example.com", role=UserRole.admin)
        user_data3 = UserCreate(name="User Three", email="user3@example.com", role=UserRole.student)
        
        user1 = UserService.create_user(user_data1)
        user2 = UserService.create_user(user_data2)
        user3 = UserService.create_user(user_data3)
        
        users = UserService.get_all_users()
        
        assert len(users) == 3
        user_ids = [u.id for u in users]
        assert user1.id in user_ids
        assert user2.id in user_ids
        assert user3.id in user_ids
    
    def test_get_all_users_returns_list(self):
        """Test that get_all_users returns a list"""
        users = UserService.get_all_users()
        
        assert isinstance(users, list)
