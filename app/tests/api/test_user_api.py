import pytest


class TestCreateUser:
    """Tests for POST /users/ endpoint"""
    
    def test_create_user_success(self, client):
        """Test successfully creating a user with valid data"""
        user_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "role": "student"
        }
        response = client.post("/users/", json=user_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "John Doe"
        assert data["email"] == "john@example.com"
        assert data["role"] == "student"
        assert "id" in data
        assert isinstance(data["id"], int)
    
    def test_create_admin_user(self, client):
        """Test creating an admin user"""
        user_data = {
            "name": "Admin User",
            "email": "admin@example.com",
            "role": "admin"
        }
        response = client.post("/users/", json=user_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["role"] == "admin"
    
    def test_create_user_invalid_email(self, client):
        """Test creating user with invalid email format"""
        user_data = {
            "name": "John Doe",
            "email": "invalid-email",
            "role": "student"
        }
        response = client.post("/users/", json=user_data)
        
        assert response.status_code == 422
    
    def test_create_user_invalid_role(self, client):
        """Test creating user with invalid role"""
        user_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "role": "teacher"  # Invalid role
        }
        response = client.post("/users/", json=user_data)
        
        assert response.status_code == 422
    
    def test_create_user_missing_name(self, client):
        """Test creating user without name"""
        user_data = {
            "email": "john@example.com",
            "role": "student"
        }
        response = client.post("/users/", json=user_data)
        
        assert response.status_code == 422
    
    def test_create_user_missing_email(self, client):
        """Test creating user without email"""
        user_data = {
            "name": "John Doe",
            "role": "student"
        }
        response = client.post("/users/", json=user_data)
        
        assert response.status_code == 422
    
    def test_create_user_empty_name(self, client):
        """Test creating user with empty name"""
        user_data = {
            "name": "",
            "email": "john@example.com",
            "role": "student"
        }
        response = client.post("/users/", json=user_data)
        
        assert response.status_code == 422


class TestGetUser:
    """Tests for GET /users/{user_id} endpoint"""
    
    def test_get_user_success(self, client, sample_student_user):
        """Test retrieving an existing user"""
        user_id = sample_student_user.id
        response = client.get(f"/users/{user_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["name"] == sample_student_user.name
        assert data["email"] == sample_student_user.email
        assert data["role"] == sample_student_user.role
    
    def test_get_user_not_found(self, client):
        """Test retrieving a non-existent user"""
        response = client.get("/users/999")
        
        assert response.status_code == 404
    
    def test_get_admin_user(self, client, sample_admin_user):
        """Test retrieving an admin user"""
        user_id = sample_admin_user.id
        response = client.get(f"/users/{user_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["role"] == "admin"
