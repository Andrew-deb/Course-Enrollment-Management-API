import pytest


class TestGetAllCourses:
    """Tests for GET /courses/ endpoint (Public Access)"""
    
    def test_get_all_courses_empty(self, client):
        """Test retrieving courses when none exist"""
        response = client.get("/courses/")
        
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_all_courses_with_data(self, client, sample_course, sample_course2):
        """Test retrieving all courses when multiple exist"""
        response = client.get("/courses/")
        
        assert response.status_code == 200
        courses = response.json()
        assert len(courses) == 2
        assert any(c["code"] == "CS101" for c in courses)
        assert any(c["code"] == "CS201" for c in courses)
    
    def test_get_all_courses_no_auth_required(self, client, sample_course):
        """Test that no authentication/role is required"""
        response = client.get("/courses/")
        
        assert response.status_code == 200
        assert len(response.json()) == 1


class TestGetCourseById:
    """Tests for GET /courses/{course_id} endpoint (Public Access)"""
    
    def test_get_course_success(self, client, sample_course):
        """Test retrieving an existing course"""
        course_id = sample_course.id
        response = client.get(f"/courses/{course_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == course_id
        assert data["title"] == sample_course.title
        assert data["code"] == sample_course.code
    
    def test_get_course_not_found(self, client):
        """Test retrieving a non-existent course"""
        response = client.get("/courses/999")
        
        assert response.status_code == 404
    
    def test_get_course_no_auth_required(self, client, sample_course):
        """Test that no authentication/role is required"""
        course_id = sample_course.id
        response = client.get(f"/courses/{course_id}")
        
        assert response.status_code == 200


class TestCreateCourse:
    """Tests for POST /courses/ endpoint (Admin Only)"""
    
    def test_create_course_as_admin_success(self, client, sample_admin_user):
        """Test admin can successfully create a course"""
        course_data = {
            "title": "Web Development",
            "code": "WEB101"
        }
        response = client.post(
            "/courses/",
            json=course_data,
            params={"user_id": sample_admin_user.id}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Web Development"
        assert data["code"] == "WEB101"
        assert "id" in data
        assert isinstance(data["id"], int)
    
    def test_create_course_as_student_forbidden(self, client, sample_student_user):
        """Test student cannot create a course (403 Forbidden)"""
        course_data = {
            "title": "Web Development",
            "code": "WEB101"
        }
        response = client.post(
            "/courses/",
            json=course_data,
            params={"user_id": sample_student_user.id}
        )
        
        assert response.status_code == 403
    
    def test_create_course_missing_title(self, client, sample_admin_user):
        """Test creating course without title"""
        course_data = {
            "code": "WEB101"
        }
        response = client.post(
            "/courses/",
            json=course_data,
            params={"user_id": sample_admin_user.id}
        )
        
        assert response.status_code == 422
    
    def test_create_course_missing_code(self, client, sample_admin_user):
        """Test creating course without code"""
        course_data = {
            "title": "Web Development"
        }
        response = client.post(
            "/courses/",
            json=course_data,
            params={"user_id": sample_admin_user.id}
        )
        
        assert response.status_code == 422
    
    def test_create_course_duplicate_code(self, client, sample_admin_user, sample_course):
        """Test creating course with duplicate code (400)"""
        course_data = {
            "title": "Another Course",
            "code": sample_course.code  # Duplicate code
        }
        response = client.post(
            "/courses/",
            json=course_data,
            params={"user_id": sample_admin_user.id}
        )
        
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"].lower()


class TestUpdateCourse:
    """Tests for PUT /courses/{course_id} endpoint (Admin Only)"""
    
    def test_update_course_as_admin_success(self, client, sample_admin_user, sample_course):
        """Test admin can successfully update a course"""
        course_id = sample_course.id
        update_data = {
            "title": "Updated Title",
            "code": "CS101-NEW"
        }
        response = client.put(
            f"/courses/{course_id}",
            json=update_data,
            params={"user_id": sample_admin_user.id}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["code"] == "CS101-NEW"
        assert data["id"] == course_id
    
    def test_update_course_partial_title_only(self, client, sample_admin_user, sample_course):
        """Test partial update (title only)"""
        course_id = sample_course.id
        original_code = sample_course.code
        update_data = {
            "title": "Updated Title Only"
        }
        response = client.put(
            f"/courses/{course_id}",
            json=update_data,
            params={"user_id": sample_admin_user.id}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title Only"
        assert data["code"] == original_code  # Code unchanged
    
    def test_update_course_partial_code_only(self, client, sample_admin_user, sample_course):
        """Test partial update (code only)"""
        course_id = sample_course.id
        original_title = sample_course.title
        update_data = {
            "code": "CS101-UPDATED"
        }
        response = client.put(
            f"/courses/{course_id}",
            json=update_data,
            params={"user_id": sample_admin_user.id}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == "CS101-UPDATED"
        assert data["title"] == original_title  # Title unchanged
    
    def test_update_course_as_student_forbidden(self, client, sample_student_user, sample_course):
        """Test student cannot update a course (403 Forbidden)"""
        course_id = sample_course.id
        update_data = {
            "title": "Updated Title"
        }
        response = client.put(
            f"/courses/{course_id}",
            json=update_data,
            params={"user_id": sample_student_user.id}
        )
        
        assert response.status_code == 403
    
    def test_update_course_not_found(self, client, sample_admin_user):
        """Test updating non-existent course (404)"""
        update_data = {
            "title": "Updated Title"
        }
        response = client.put(
            "/courses/999",
            json=update_data,
            params={"user_id": sample_admin_user.id}
        )
        
        assert response.status_code == 404
    
    def test_update_course_duplicate_code(self, client, sample_admin_user, sample_course, sample_course2):
        """Test updating course with code that already exists on another course"""
        course_id = sample_course.id
        update_data = {
            "code": sample_course2.code  # Use code from another course
        }
        response = client.put(
            f"/courses/{course_id}",
            json=update_data,
            params={"user_id": sample_admin_user.id}
        )
        
        assert response.status_code == 400
    
    def test_update_course_same_code_allowed(self, client, sample_admin_user, sample_course):
        """Test updating course keeping the same code (should be allowed)"""
        course_id = sample_course.id
        update_data = {
            "title": "Updated Title",
            "code": sample_course.code  # Same code
        }
        response = client.put(
            f"/courses/{course_id}",
            json=update_data,
            params={"user_id": sample_admin_user.id}
        )
        
        assert response.status_code == 200


class TestDeleteCourse:
    """Tests for DELETE /courses/{course_id} endpoint (Admin Only)"""
    
    def test_delete_course_as_admin_success(self, client, sample_admin_user, sample_course):
        """Test admin can successfully delete a course"""
        course_id = sample_course.id
        response = client.delete(
            f"/courses/{course_id}",
            params={"user_id": sample_admin_user.id}
        )
        
        assert response.status_code == 204
        
        # Verify course was actually deleted
        get_response = client.get(f"/courses/{course_id}")
        assert get_response.status_code == 404
    
    def test_delete_course_as_student_forbidden(self, client, sample_student_user, sample_course):
        """Test student cannot delete a course (403 Forbidden)"""
        course_id = sample_course.id
        response = client.delete(
            f"/courses/{course_id}",
            params={"user_id": sample_student_user.id}
        )
        
        assert response.status_code == 403
        
        # Verify course still exists
        get_response = client.get(f"/courses/{course_id}")
        assert get_response.status_code == 200
    
    def test_delete_course_not_found(self, client, sample_admin_user):
        """Test deleting non-existent course (404)"""
        response = client.delete(
            "/courses/999",
            params={"user_id": sample_admin_user.id}
        )
        
        assert response.status_code == 404
    
    def test_delete_course_invalid_user(self, client, sample_course):
        """Test deleting course with non-existent user (404)"""
        course_id = sample_course.id
        response = client.delete(
            f"/courses/{course_id}",
            params={"user_id": 999}
        )
        
        assert response.status_code == 404
