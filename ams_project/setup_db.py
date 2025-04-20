import os
import django
import sys

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ams_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import Course, Faculty, Student, CourseStudent

User = get_user_model()

def setup_database():
    print("Setting up initial database...")
    
    # Create admin user
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword',
            role=User.ADMIN
        )
        print(f"Created admin user: {admin_user.username}")
    
    # Create faculty user
    faculty_user = User.objects.filter(username='faculty').first()
    if not faculty_user:
        faculty_user = User.objects.create_user(
            username='faculty',
            email='faculty@example.com',
            password='facultypassword',
            first_name='John',
            last_name='Doe',
            role=User.FACULTY
        )
        print(f"Created faculty user: {faculty_user.username}")
    
    # Create faculty profile
    try:
        faculty = Faculty.objects.get(user=faculty_user)
    except Faculty.DoesNotExist:
        faculty = Faculty.objects.create(
            user=faculty_user,
            faculty_id=f"F{faculty_user.id:06d}",
            department='Computer Science',
            designation='Professor'
        )
        print("Created faculty profile")

    # Create student1 user
    student_user = User.objects.filter(username='student').first()
    if not student_user:
        student_user = User.objects.create_user(
            username='student',
            email='student@example.com',
            password='studentpassword',
            first_name='Jane',
            last_name='Smith',
            role=User.STUDENT
        )
        print(f"Created student user: {student_user.username}")
    
    # Create student1 profile
    try:
        student = Student.objects.get(user=student_user)
    except Student.DoesNotExist:
        student = Student.objects.create(
            user=student_user,
            student_id=f"S{student_user.id:06d}",
            department='Computer Science',
            year_of_admission=2023
        )
        print("Created student profile")

    # Create second student
    student2_user = User.objects.filter(username='student2').first()
    if not student2_user:
        student2_user = User.objects.create_user(
            username='student2',
            email='student2@example.com',
            password='student2password',
            first_name='Alice',
            last_name='Wonder',
            role=User.STUDENT
        )
        print(f"Created student user: {student2_user.username}")
    
    try:
        student2 = Student.objects.get(user=student2_user)
    except Student.DoesNotExist:
        student2 = Student.objects.create(
            user=student2_user,
            student_id=f"S{student2_user.id:06d}",
            department='Computer Science',
            year_of_admission=2023
        )
        print("Created second student profile")

    # Create course and enroll students
    course = Course.objects.filter(course_code='CS101').first()
    if not course:
        course = Course.objects.create(
            course_code='CS101',
            course_name='Introduction to Computer Science',
            faculty=faculty,
            description='A beginner-friendly introduction to computer science principles',
            semester='Fall',
            year=2023,
            start_date='2023-09-01',
            end_date='2023-12-15'
        )
        print(f"Created sample course: {course.course_code}")

    # Enroll students
    CourseStudent.objects.get_or_create(course=course, student=student)
    CourseStudent.objects.get_or_create(course=course, student=student2)
    print("Enrolled both students into CS101")

    print("Database setup complete!")

if __name__ == "__main__":
    setup_database()
