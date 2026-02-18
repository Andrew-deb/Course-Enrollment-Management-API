# Course Enrollment Management API

A RESTful API built with FastAPI for managing a course enrollment system with role-based access control (admin and student roles).

## Features

- **User Management**: Create and retrieve users with role-based access (student/admin)
- **Course Management**: Admin-only CRUD operations for courses with unique code validation
- **Enrollment Management**: Students can enroll and deregister from courses
- **Admin Oversight**: Admins can view all enrollments and force-deregister students
- **Role-Based Access Control**: Endpoints enforce student and admin role restrictions
- **Data Validation**: Input validation for all entities
- **In-Memory Storage**: Uses in-memory data structures (no database required)

## Project Structure

```
app/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Project dependencies
├── README.md              # This file
├── api/
│   ├── __init__.py
│   ├── deps.py            # Dependency injection (role-based access)
│   └── v1/
│       ├── __init__.py
│       ├── user.py        # User endpoints
│       ├── course.py       # Course endpoints
│       └── enrollment.py   # Enrollment endpoints
├── core/
│   ├── __init__.py
│   └── db.py              # In-memory data storage
├── schemas/
│   ├── __init__.py
│   ├── user.py            # User data models
│   ├── course.py          # Course data models
│   └── enrollment.py      # Enrollment data models
├── service/
│   ├── __init__.py
│   ├── user.py            # User business logic
│   ├── course.py          # Course business logic
│   └── enrollment.py      # Enrollment business logic
└── tests/
    ├── __init__.py
    ├── conftest.py        # Pytest configuration and fixtures
    ├── api/               # API endpoint tests
    │   ├── test_user_api.py
    │   ├── test_course_api.py
    │   └── test_enrollment_api.py
    └── unit/              # Unit tests for services
        ├── test_user_service.py
        ├── test_course_service.py
        └── test_enrollment_service.py
```

## Separation of Concerns

This project keeps HTTP concerns in the route layer and business rules in the service layer:

- **Service layer** handles domain logic and raises domain-specific errors using built-in exceptions like `ValueError` and `KeyError`.
- **Route layer** catches service exceptions and converts them into `HTTPException` responses with the appropriate HTTP status codes.
- **Schema layer** defines request/response models and validation rules for consistent data shapes.
- **Core layer** holds shared infrastructure concerns like in-memory storage.
- **Dependency layer** enforces role-based access control through injected checks.
- **Test layer** validates both the API endpoints and service logic with isolated unit and integration tests.

This keeps the core logic framework-agnostic and makes error handling consistent across endpoints.

## Installation

### Prerequisites

- Python 3.13 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or navigate to the project directory**:
   ```bash
   cd Course-Enrollment-Management-API
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - **Windows (PowerShell)**:
     ```bash
     .\venv\Scripts\Activate.ps1
     ```
   - **Windows (Command Prompt)**:
     ```bash
     venv\Scripts\activate.bat
     ```
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r app/requirements.txt
   ```

## Running the API

### Start the Development Server

Start the API server using Uvicorn:

```bash
python -m uvicorn app.main:app --reload
```

The server will be available at:
- **Base URL**: `http://localhost:8000`
- **API Documentation (Swagger UI)**: `http://localhost:8000/docs`
- **Alternative Documentation (ReDoc)**: `http://localhost:8000/redoc`

### API Endpoints

#### User Endpoints (Public)
- `POST /users/` - Create a user
- `GET /users/{user_id}` - Get user by ID

#### Course Endpoints
- `GET /courses/` - Get all courses (public)
- `GET /courses/{course_id}` - Get course by ID (public)
- `POST /courses/` - Create course (admin only)
- `PUT /courses/{course_id}` - Update course (admin only)
- `DELETE /courses/{course_id}` - Delete course (admin only)

#### Enrollment Endpoints
- `POST /enrollments/` - Enroll in course (student only)
- `DELETE /enrollments/{enrollment_id}` - Deregister from course (student only)
- `GET /enrollments/my-enrollments` - Get my enrollments (student only)
- `GET /enrollments/` - Get all enrollments (admin only)
- `GET /enrollments/course/{course_id}` - Get enrollments by course (admin only)
- `DELETE /enrollments/force/{enrollment_id}` - Force deregister student (admin only)

### Example API Requests

#### Create a Student User
```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "role": "student"
  }'
```

#### Create a Course (Admin Only)
```bash
curl -X POST "http://localhost:8000/courses/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Introduction to Programming",
    "code": "CS101"
  }' \
  -G --data-urlencode "user_id=1"
```
*Note: Pass `user_id` as a query parameter. User must have admin role.*

#### Enroll in a Course (Student Only)
```bash
curl -X POST "http://localhost:8000/enrollments/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 2,
    "course_id": 1
  }' \
  -G --data-urlencode "user_id=2"
```
*Note: `user_id` must have student role.*

#### Get All Courses (Public)
```bash
curl "http://localhost:8000/courses/"
```

## Running the Tests

### Prerequisites

Tests use pytest and are configured with fixtures for test isolation and reusable test data.

### Run All Tests

```bash
pytest app/tests/ -v
```

### Run Specific Test Categories

**API Tests Only**:
```bash
pytest app/tests/api/ -v
```

**Unit Tests Only**:
```bash
pytest app/tests/unit/ -v
```

**Specific Test File**:
```bash
pytest app/tests/api/test_user_api.py -v
```

**Specific Test Class**:
```bash
pytest app/tests/api/test_course_api.py::TestCreateCourse -v
```

**Specific Test Case**:
```bash
pytest app/tests/api/test_enrollment_api.py::TestCreateEnrollment::test_enroll_as_student_success -v
```

### Test Output Options

**Quiet Mode** (summary only):
```bash
pytest app/tests/ -q
```

**With Coverage Report**:
```bash
pytest app/tests/ --cov=app --cov-report=html
```

**Stop on First Failure**:
```bash
pytest app/tests/ -x
```

**Show Print Statements**:
```bash
pytest app/tests/ -s
```

## Test Coverage

The test suite includes **116 comprehensive tests** across all endpoints and services:

### API Tests (58 tests)
- **User API**: 10 tests covering user creation and retrieval
- **Course API**: 23 tests including role-based access, CRUD operations, and validation
- **Enrollment API**: 25 tests covering student/admin operations and business rules

### Unit Tests (58 tests)
- **UserService**: 11 tests for user operations
- **CourseService**: 20 tests including duplicate handling and partial updates
- **EnrollmentService**: 27 tests covering enrollment creation, retrieval, and deletion

### Test Coverage Summary
- ✅ All 11 API endpoints tested
- ✅ Role-based behavior verified (student vs admin vs public)
- ✅ Input validation tested (email format, unique codes, etc.)
- ✅ Business logic validated (duplicate prevention, relationships, etc.)
- ✅ Error handling tested (404, 403, 400, 422 status codes)
- ✅ **100% pass rate**: 116/116 tests passing

## Data Models

### User
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "role": "student"
}
```

Roles: `"student"` or `"admin"`

### Course
```json
{
  "id": 1,
  "title": "Introduction to Programming",
  "code": "CS101"
}
```

### Enrollment
```json
{
  "id": 1,
  "user_id": 2,
  "course_id": 1
}
```

## Business Rules

### User Management
- Name must not be empty
- Email must be in valid email format
- Role must be either "student" or "admin"

### Course Management
- Title must not be empty
- Course code must not be empty and must be unique
- Only admins can create, update, or delete courses
- Any user can view all courses

### Enrollment Management
- Only students can enroll/deregister
- A student cannot enroll in the same course more than once
- Enrollment requires both user and course to exist
- Admins can view all enrollments and force-deregister students
- Students can only see their own enrollments

## Important Notes

- **In-Memory Storage**: All data is stored in memory and will be lost when the application restarts
- **No Authentication**: The API assumes the user role is provided in the request. No token-based authentication is implemented
- **Validation**: Pydantic is used for request validation. Invalid requests return 422 status code
- **Error Handling**: Appropriate HTTP status codes are used:
  - 200: Success
  - 201: Created
  - 204: No Content (successful deletion)
  - 400: Bad Request (business logic violation)
  - 403: Forbidden (insufficient permissions)
  - 404: Not Found
  - 422: Unprocessable Entity (validation error)

## Troubleshooting

### Port Already In Use
If port 8000 is already in use, start the server on a different port:
```bash
python -m uvicorn app.main:app --reload --port 8001
```

### Import Errors
Ensure the virtual environment is activated and dependencies are installed:
```bash
pip install -r app/requirements.txt
```

### Tests Failing
Make sure you're running pytest from the project root directory:
```bash
pytest app/tests/ -v
```

## Development

### Adding New Tests
Tests are located in `app/tests/`. Follow the existing structure:
- API tests in `app/tests/api/`
- Unit tests in `app/tests/unit/`

Test fixtures are defined in `app/tests/conftest.py` and automatically available to all tests.

### Code Style
The project follows PEP 8 conventions. Use consistent formatting and meaningful variable names.

## License

This project is part of Alt School curriculum.

## Support

For issues or questions about the API, refer to the FastAPI documentation at https://fastapi.tiangolo.com/
