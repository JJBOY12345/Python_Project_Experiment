# core/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    """Custom User model with role-based authentication"""
    STUDENT = 'student'
    FACULTY = 'faculty'
    ADMIN = 'admin'
    
    ROLE_CHOICES = [
        (STUDENT, 'Student'),
        (FACULTY, 'Faculty'),
        (ADMIN, 'Admin'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=STUDENT)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_student(self):
        return self.role == self.STUDENT
    
    @property
    def is_faculty(self):
        return self.role == self.FACULTY
    
    @property
    def is_admin_user(self):
        return self.role == self.ADMIN

class Student(models.Model):
    """Student model linked to User model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    year_of_admission = models.IntegerField()
    
    def __str__(self):
        return f"{self.student_id} - {self.user.get_full_name()}"

class Faculty(models.Model):
    """Faculty model linked to User model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='faculty_profile')
    faculty_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.faculty_id} - {self.user.get_full_name()}"

class Course(models.Model):
    """Course model"""
    course_code = models.CharField(max_length=20, unique=True)
    course_name = models.CharField(max_length=200)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, related_name='courses')
    description = models.TextField(blank=True)
    semester = models.CharField(max_length=20)
    year = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    
    def __str__(self):
        return f"{self.course_code} - {self.course_name}"

class CourseStudent(models.Model):
    """Course-Student relationship model"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    
    class Meta:
        unique_together = ('course', 'student')
    
    def __str__(self):
        return f"{self.student} enrolled in {self.course}"

class AttendanceRecord(models.Model):
    """Attendance record model"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendance_records')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('excused', 'Excused'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    marked_by = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('course', 'student', 'date')
    
    def __str__(self):
        return f"{self.student} - {self.course} - {self.date} - {self.status}"

class AttendanceCorrectionRequest(models.Model):
    """Attendance correction request model"""
    attendance_record = models.ForeignKey(AttendanceRecord, on_delete=models.CASCADE, related_name='correction_requests')
    requested_by = models.ForeignKey(Student, on_delete=models.CASCADE)
    requested_status = models.CharField(max_length=10, choices=AttendanceRecord.STATUS_CHOICES)
    reason = models.TextField()
    supporting_document = models.FileField(upload_to='correction_docs/', blank=True, null=True)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    reviewed_by = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True)
    review_comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Correction for {self.attendance_record} - {self.status}"

class ExcuseRequest(models.Model):
    """Excuse absence request model"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='excuse_requests')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    supporting_document = models.FileField(upload_to='excuse_docs/', blank=True, null=True)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    reviewed_by = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True)
    review_comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Excuse request by {self.student} for {self.course} - {self.status}"

class Notification(models.Model):
    """Notification model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=100)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.user}"