import pytest
from app.schemas.enrollment import EnrollmentCreate
from app.service.enrollment import EnrollmentService


class TestCreateEnrollment:
    """Tests for POST /enrollments/ endpoint (Student Only)"""
    
    def test_enroll_as_student_success(self, client, sample_student_user, sample_course):
        """Test student can successfully enroll in a course"""
        enrollment_data = {
            "user_id": sample_student_user.id,
            "course_id": sample_course.id
        }
        response = client.post(
            "/enrollments/",
            json=enrollment_data,
            params={"user_id": sample_student_user.id}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["user_id"] == sample_student_user.id
        assert data["course_id"] == sample_course.id
        assert "id" in data
        assert isinstance(data["id"], int)
    
    def test_enroll_as_admin_forbidden(self, client, sample_admin_user, sample_course):
        """Test admin cannot enroll (403 Forbidden)"""
        enrollment_data = {
            "user_id": sample_admin_user.id,
            "course_id": sample_course.id
        }
        response = client.post(
            "/enrollments/",
            json=enrollment_data,
            params={"user_id": sample_admin_user.id}
        )
        
        assert response.status_code == 403
    
    def test_enroll_invalid_user(self, client, sample_student_user, sample_course):
        """Test enrolling non-existent user (404)"""
        enrollment_data = {
            "user_id": 999,
            "course_id": sample_course.id
        }
        response = client.post(
            "/enrollments/",
            json=enrollment_data,
            params={"user_id": sample_student_user.id}
        )
        
        assert response.status_code == 404
    
    def test_enroll_invalid_course(self, client, sample_student_user):
        """Test enrolling in non-existent course (404)"""
        enrollment_data = {
            "user_id": sample_student_user.id,
            "course_id": 999
        }
        response = client.post(
            "/enrollments/",
            json=enrollment_data,
            params={"user_id": sample_student_user.id}
        )
        
        assert response.status_code == 404
    
    def test_enroll_duplicate_enrollment(self, client, sample_student_user, sample_course):
        """Test preventing duplicate enrollment (400)"""
        enrollment_data = {
            "user_id": sample_student_user.id,
            "course_id": sample_course.id
        }
        
        # First enrollment succeeds
        response1 = client.post(
            "/enrollments/",
            json=enrollment_data,
            params={"user_id": sample_student_user.id}
        )
        assert response1.status_code == 201
        
        # Second enrollment fails
        response2 = client.post(
            "/enrollments/",
            json=enrollment_data,
            params={"user_id": sample_student_user.id}
        )
        assert response2.status_code == 400
        assert "already enrolled" in response2.json()["detail"].lower()
    
    def test_enroll_missing_user_id(self, client, sample_student_user):
        """Test enrollment without user_id"""
        enrollment_data = {
            "course_id": 1
        }
        response = client.post(
            "/enrollments/",
            json=enrollment_data,
            params={"user_id": sample_student_user.id}
        )
        
        assert response.status_code == 422
    
    def test_enroll_missing_course_id(self, client, sample_student_user):
        """Test enrollment without course_id"""
        enrollment_data = {
            "user_id": sample_student_user.id
        }
        response = client.post(
            "/enrollments/",
            json=enrollment_data,
            params={"user_id": sample_student_user.id}
        )
        
        assert response.status_code == 422


class TestDeregisterEnrollment:
    """Tests for DELETE /enrollments/{enrollment_id} endpoint (Student Only)"""
    
    def test_deregister_as_student_success(self, client, sample_student_user, sample_course):
        """Test student can successfully deregister from a course"""
        # First enroll
        enrollment = EnrollmentService.create_enrollment(
            EnrollmentCreate(user_id=sample_student_user.id, course_id=sample_course.id)
        )
        
        # Then deregister
        response = client.delete(
            f"/enrollments/{enrollment.id}",
            params={"user_id": sample_student_user.id}
        )
        
        assert response.status_code == 204
        
        # Verify enrollment was deleted
        all_enrollments = EnrollmentService.get_all_enrollments()
        assert len(all_enrollments) == 0
    
    def test_deregister_as_admin_forbidden(self, client, sample_admin_user, sample_student_user, sample_course):
        """Test admin cannot deregister using student endpoint (403 Forbidden)"""
        # Create enrollment
        enrollment = EnrollmentService.create_enrollment(
            EnrollmentCreate(user_id=sample_student_user.id, course_id=sample_course.id)
        )
        
        # Admin tries to deregister
        response = client.delete(
            f"/enrollments/{enrollment.id}",
            params={"user_id": sample_admin_user.id}
        )
        
        assert response.status_code == 403
    
    def test_deregister_not_found(self, client, sample_student_user):
        """Test deregistering non-existent enrollment (404)"""
        response = client.delete(
            "/enrollments/999",
            params={"user_id": sample_student_user.id}
        )
        
        assert response.status_code == 404
    
    # def test_deregister_invalid_user(self, client, sample_student_user, sample_course):
    #     """Test deregistering with invalid user (404)"""
    #     # Create enrollment
    #     enrollment = EnrollmentService.create_enrollment(
    #         EnrollmentCreate(user_id=sample_student_user.id, course_id=sample_course.id)
    #     )
        
    #     # Try to deregister with invalid user
    #     response = client.delete(
    #         f"/enrollments/{enrollment.id}",
    #         params={"user_id": 999}
    #     )
        
        assert response.status_code == 404


class TestGetMyEnrollments:
    """Tests for GET /enrollments/my-enrollments endpoint (Student Only)"""
    
    def test_get_my_enrollments_empty(self, client, sample_student_user):
        """Test getting enrollments when student has none"""
        response = client.get(
            "/enrollments/my-enrollments",
            params={"user_id": sample_student_user.id}
        )
        
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_my_enrollments_single(self, client, sample_student_user, sample_course):
        """Test getting enrollments when student has one"""
        # Create enrollment
        enrollment = EnrollmentService.create_enrollment(
            EnrollmentCreate(user_id=sample_student_user.id, course_id=sample_course.id)
        )
        
        response = client.get(
            "/enrollments/my-enrollments",
            params={"user_id": sample_student_user.id}
        )
        
        assert response.status_code == 200
        enrollments = response.json()
        assert len(enrollments) == 1
        assert enrollments[0]["id"] == enrollment.id
        assert enrollments[0]["user_id"] == sample_student_user.id
        assert enrollments[0]["course_id"] == sample_course.id
    
    def test_get_my_enrollments_multiple(self, client, sample_student_user, sample_course, sample_course2):
        """Test getting enrollments when student has multiple"""
        # Create multiple enrollments
        enrollment1 = EnrollmentService.create_enrollment(
            EnrollmentCreate(user_id=sample_student_user.id, course_id=sample_course.id)
        )
        enrollment2 = EnrollmentService.create_enrollment(
            EnrollmentCreate(user_id=sample_student_user.id, course_id=sample_course2.id)
        )
        
        response = client.get(
            "/enrollments/my-enrollments",
            params={"user_id": sample_student_user.id}
        )
        
        assert response.status_code == 200
        enrollments = response.json()
        assert len(enrollments) == 2
        enrollment_ids = [e["id"] for e in enrollments]
        assert enrollment1.id in enrollment_ids
        assert enrollment2.id in enrollment_ids
    
    def test_get_my_enrollments_as_admin_forbidden(self, client, sample_admin_user):
        """Test admin cannot access student endpoint (403 Forbidden)"""
        response = client.get(
            "/enrollments/my-enrollments",
            params={"user_id": sample_admin_user.id}
        )
        
        assert response.status_code == 403


class TestGetAllEnrollments:
    """Tests for GET /enrollments/ endpoint (Admin Only)"""
    
    def test_get_all_enrollments_as_admin_empty(self, client, sample_admin_user):
        """Test admin getting all enrollments when none exist"""
        response = client.get(
            "/enrollments/",
            params={"user_id": sample_admin_user.id}
        )
        
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_all_enrollments_as_admin_with_data(self, client, sample_admin_user, 
                                                     sample_student_user, sample_student_user2,
                                                     sample_course, sample_course2):
        """Test admin getting all enrollments across multiple users"""
        # Create enrollments for different students
        enrollment1 = EnrollmentService.create_enrollment(
            EnrollmentCreate(user_id=sample_student_user.id, course_id=sample_course.id)
        )
        enrollment2 = EnrollmentService.create_enrollment(
            EnrollmentCreate(user_id=sample_student_user2.id, course_id=sample_course.id)
        )
        enrollment3 = EnrollmentService.create_enrollment(
            EnrollmentCreate(user_id=sample_student_user.id, course_id=sample_course2.id)
        )
        
        response = client.get(
            "/enrollments/",
            params={"user_id": sample_admin_user.id}
        )
        
        assert response.status_code == 200
        enrollments = response.json()
        assert len(enrollments) == 3
        enrollment_ids = [e["id"] for e in enrollments]
        assert enrollment1.id in enrollment_ids
        assert enrollment2.id in enrollment_ids
        assert enrollment3.id in enrollment_ids
    
    def test_get_all_enrollments_as_student_forbidden(self, client, sample_student_user):
        """Test student cannot get all enrollments (403 Forbidden)"""
        response = client.get(
            "/enrollments/",
            params={"user_id": sample_student_user.id}
        )
        
        assert response.status_code == 403


class TestGetEnrollmentsByCourse:
    """Tests for GET /enrollments/course/{course_id} endpoint (Admin Only)"""
    
    def test_get_enrollments_by_course_as_admin_empty(self, client, sample_admin_user, sample_course):
        """Test admin getting enrollments for course with no enrollments"""
        response = client.get(
            f"/enrollments/course/{sample_course.id}",
            params={"user_id": sample_admin_user.id}
        )
        
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_enrollments_by_course_as_admin_single(self, client, sample_admin_user,
                                                        sample_student_user, sample_course):
        """Test admin getting enrollments for course with one enrollment"""
        enrollment = EnrollmentService.create_enrollment(
            EnrollmentCreate(user_id=sample_student_user.id, course_id=sample_course.id)
        )
        
        response = client.get(
            f"/enrollments/course/{sample_course.id}",
            params={"user_id": sample_admin_user.id}
        )
        
        assert response.status_code == 200
        enrollments = response.json()
        assert len(enrollments) == 1
        assert enrollments[0]["id"] == enrollment.id
        assert enrollments[0]["course_id"] == sample_course.id
    
    def test_get_enrollments_by_course_as_admin_multiple(self, client, sample_admin_user,
                                                          sample_student_user, sample_student_user2,
                                                          sample_course, sample_course2):
        """Test admin getting enrollments for course with multiple students"""
        # Multiple students enroll in same course
        enrollment1 = EnrollmentService.create_enrollment(
            EnrollmentCreate(user_id=sample_student_user.id, course_id=sample_course.id)
        )
        enrollment2 = EnrollmentService.create_enrollment(
            EnrollmentCreate(user_id=sample_student_user2.id, course_id=sample_course.id)
        )
        # Also enroll one student in different course
        enrollment3 = EnrollmentService.create_enrollment(
            EnrollmentCreate(user_id=sample_student_user.id, course_id=sample_course2.id)
        )
        
        response = client.get(
            f"/enrollments/course/{sample_course.id}",
            params={"user_id": sample_admin_user.id}
        )
        
        assert response.status_code == 200
        enrollments = response.json()
        assert len(enrollments) == 2  # Only enrollments for sample_course
        enrollment_ids = [e["id"] for e in enrollments]
        assert enrollment1.id in enrollment_ids
        assert enrollment2.id in enrollment_ids
        assert enrollment3.id not in enrollment_ids  # Different course
    
    def test_get_enrollments_by_course_as_student_forbidden(self, client, sample_student_user, sample_course):
        """Test student cannot get enrollments by course (403 Forbidden)"""
        response = client.get(
            f"/enrollments/course/{sample_course.id}",
            params={"user_id": sample_student_user.id}
        )
        
        assert response.status_code == 403
    
    def test_get_enrollments_by_course_not_found(self, client, sample_admin_user):
        """Test getting enrollments for non-existent course (404)"""
        response = client.get(
            "/enrollments/course/999",
            params={"user_id": sample_admin_user.id}
        )
        
        assert response.status_code == 404


class TestForceDeregisterEnrollment:
    """Tests for DELETE /enrollments/force/{enrollment_id} endpoint (Admin Only)"""
    
    def test_force_deregister_as_admin_success(self, client, sample_admin_user, 
                                                sample_student_user, sample_course):
        """Test admin can force deregister a student"""
        # Create enrollment
        enrollment = EnrollmentService.create_enrollment(
            EnrollmentCreate(user_id=sample_student_user.id, course_id=sample_course.id)
        )
        
        # Admin force deregisters
        response = client.delete(
            f"/enrollments/force/{enrollment.id}",
            params={"user_id": sample_admin_user.id}
        )
        
        assert response.status_code == 204
        
        # Verify enrollment was deleted
        all_enrollments = EnrollmentService.get_all_enrollments()
        assert len(all_enrollments) == 0
    
    def test_force_deregister_as_student_forbidden(self, client, sample_student_user, 
                                                     sample_student_user2, sample_course):
        """Test student cannot force deregister (403 Forbidden)"""
        # Create enrollment
        enrollment = EnrollmentService.create_enrollment(
            EnrollmentCreate(user_id=sample_student_user2.id, course_id=sample_course.id)
        )
        
        # Student tries to force deregister
        response = client.delete(
            f"/enrollments/force/{enrollment.id}",
            params={"user_id": sample_student_user.id}
        )
        
        assert response.status_code == 403
        
        # Verify enrollment still exists
        all_enrollments = EnrollmentService.get_all_enrollments()
        assert len(all_enrollments) == 1
    
    def test_force_deregister_not_found(self, client, sample_admin_user):
        """Test force deregistering non-existent enrollment (404)"""
        response = client.delete(
            "/enrollments/force/999",
            params={"user_id": sample_admin_user.id}
        )
        
        assert response.status_code == 404
