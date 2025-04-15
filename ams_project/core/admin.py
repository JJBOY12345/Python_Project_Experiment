# core/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, Student, Faculty, Course, CourseStudent, 
    AttendanceRecord, AttendanceCorrectionRequest, 
    ExcuseRequest, Notification
)

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role Information', {'fields': ('role', 'phone_number')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Role Information', {'fields': ('role', 'phone_number', 'email')}),
    )

admin.site.register(User, CustomUserAdmin)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'get_full_name', 'department', 'year_of_admission')
    search_fields = ('student_id', 'user__username', 'user__first_name', 'user__last_name')
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Name'

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('faculty_id', 'get_full_name', 'department', 'designation')
    search_fields = ('faculty_id', 'user__username', 'user__first_name', 'user__last_name')
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Name'

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'course_name', 'faculty', 'semester', 'year')
    search_fields = ('course_code', 'course_name')
    list_filter = ('semester', 'year')

@admin.register(CourseStudent)
class CourseStudentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course')
    list_filter = ('course',)

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date', 'status', 'marked_by')
    list_filter = ('status', 'date', 'course')
    search_fields = ('student__student_id', 'student__user__first_name', 'student__user__last_name')

@admin.register(AttendanceCorrectionRequest)
class AttendanceCorrectionRequestAdmin(admin.ModelAdmin):
    list_display = ('requested_by', 'attendance_record', 'requested_status', 'status', 'created_at')
    list_filter = ('status', 'requested_status', 'created_at')

@admin.register(ExcuseRequest)
class ExcuseRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'start_date', 'end_date', 'status', 'created_at')
    list_filter = ('status', 'created_at')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
