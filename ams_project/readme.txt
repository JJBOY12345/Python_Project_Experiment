# Attendance Management System - Backend

This is the Django backend for the Attendance Management System. It provides REST API endpoints for managing student attendance with role-based functionality.

## Features

- Role-based authentication (Student, Faculty, Admin)
- JWT authentication
- MySQL database integration
- Advanced attendance management features
- Correction and excuse request workflows
- Notifications system

## Project Setup

### Prerequisites

- Python 3.8 or higher
- MySQL server
- pip package manager

### Installation

1. Clone the repository
   ```bash
   git clone <repository-url>
   cd ams_project
   ```

2. Create a virtual environment
   ```bash
   python -m venv ams_env
   source ams_env/bin/activate  # On Windows: ams_env\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the database
   - Create a MySQL database named `ams_db`
   - Update the database settings in `ams_project/settings.py` if necessary

5. Apply migrations
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Set up initial data
   ```bash
   python setup_db.py
   ```

7. Run the development server
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication

- `POST /api/register/` - Register a new user
- `POST /api/token/` - Obtain JWT token
- `POST /api/token/refresh/` - Refresh JWT token

### User Management

- `GET /api/users/` - List all users (Admin only)
- `GET /api/users/<id>/` - Get user details (Admin only)
- `GET /api/users/me/` - Get current user details

### Student Management

- `GET /api/students/` - List all students
- `POST /api/students/` - Create a new student (Admin only)
- `GET /api/students/<id>/` - Get student details

### Faculty Management

- `GET /api/faculty/` - List all faculty members
- `POST /api/faculty/` - Create a new faculty member (Admin only)
- `GET /api/faculty/<id>/` - Get faculty details

### Course Management

- `GET /api/courses/` - List all courses
- `POST /api/courses/` - Create a new course (Admin or Faculty)
- `GET /api/courses/<id>/` - Get course details
- `GET /api/courses/<id>/students/` - Get enrolled students
- `GET /api/courses/<id>/attendance/` - Get attendance records

### Attendance Management

- `GET /api/attendance/` - List all attendance records
- `POST /api/attendance/` - Create a new attendance record (Faculty or Admin)
- `GET /api/attendance/my_attendance/` - Get student's own attendance

### Correction Requests

- `GET /api/correction-requests/` - List correction requests
- `POST /api/correction-requests/` - Create a correction request (Student only)
- `GET /api/correction-requests/my_requests/` - Get student's own requests
- `GET /api/correction-requests/pending_reviews/` - Get pending reviews (Faculty only)

### Excuse Requests

- `GET /api/excuse-requests/` - List excuse requests
- `POST /api/excuse-requests/` - Create an excuse request (Student only)
- `GET /api/excuse-requests/my_requests/` - Get student's own requests
- `GET /api/excuse-requests/pending_reviews/` - Get pending reviews (Faculty only)

### Notifications

- `GET /api/notifications/` - List user's notifications
- `POST /api/notifications/mark_all_read/` - Mark all notifications as read
- `POST /api/notifications/<id>/mark_read/` - Mark specific notification as read

## Default Users

After running the setup script, the following users will be available:

1. Admin User
   - Username: admin
   - Password: adminpassword

2. Faculty User
   - Username: faculty
   - Password: facultypassword

3. Student User
   - Username: student
   - Password: studentpassword

## Next Steps

- Create a frontend application (Kivy/KivyMD) to consume these APIs
- Add QR code generation for attendance marking
- Implement advanced reporting features


REQUIREMENTS:

Django==4.2.7
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.0
django-cors-headers==4.3.0
mysqlclient==2.2.0
Pillow==10.1.0