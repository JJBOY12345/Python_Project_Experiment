from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Student, Faculty, Course, CourseStudent, 
    AttendanceRecord, AttendanceCorrectionRequest, 
    ExcuseRequest, Notification
)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone_number']
        read_only_fields = ['id']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'first_name', 'last_name', 'role', 'phone_number']

    def validate(self, data):
        if data['password'] != data.pop('confirm_password'):
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data.get('role', User.STUDENT),
            phone_number=validated_data.get('phone_number', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'user', 'student_id', 'department', 'year_of_admission']


class FacultySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Faculty
        fields = ['id', 'user', 'faculty_id', 'department', 'designation']


class CourseSerializer(serializers.ModelSerializer):
    faculty_name = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'course_code', 'course_name', 'faculty', 'faculty_name',
                  'description', 'semester', 'year', 'start_date', 'end_date']

    def get_faculty_name(self, obj):
        return obj.faculty.user.get_full_name() if obj.faculty else None


class CourseStudentSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()

    class Meta:
        model = CourseStudent
        fields = ['id', 'course', 'student', 'student_name']

    def get_student_name(self, obj):
        return obj.student.user.get_full_name()


class AttendanceRecordSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    course_name = serializers.SerializerMethodField()
    marked_by_name = serializers.SerializerMethodField()

    class Meta:
        model = AttendanceRecord
        fields = ['id', 'course', 'student', 'student_name', 'course_name',
                  'date', 'status', 'marked_by', 'marked_by_name', 'timestamp']
        read_only_fields = ['id', 'timestamp']

    def get_student_name(self, obj):
        return obj.student.user.get_full_name()

    def get_course_name(self, obj):
        return f"{obj.course.course_code} - {obj.course.course_name}"

    def get_marked_by_name(self, obj):
        return obj.marked_by.user.get_full_name() if obj.marked_by else None


class AttendanceCorrectionRequestSerializer(serializers.ModelSerializer):
    requested_by_name = serializers.SerializerMethodField()
    reviewed_by_name = serializers.SerializerMethodField()
    attendance_details = serializers.SerializerMethodField()

    class Meta:
        model = AttendanceCorrectionRequest
        fields = ['id', 'attendance_record', 'attendance_details', 'requested_by', 'requested_by_name',
                  'requested_status', 'reason', 'supporting_document', 'status',
                  'reviewed_by', 'reviewed_by_name', 'review_comments', 'created_at', 'updated_at']

    def get_requested_by_name(self, obj):
        return obj.requested_by.user.get_full_name()

    def get_reviewed_by_name(self, obj):
        return obj.reviewed_by.user.get_full_name() if obj.reviewed_by else None

    def get_attendance_details(self, obj):
        return f"{obj.attendance_record.student.student_id} - {obj.attendance_record.course.course_code} - {obj.attendance_record.date}"


class ExcuseRequestSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    course_name = serializers.SerializerMethodField()
    reviewed_by_name = serializers.SerializerMethodField()

    class Meta:
        model = ExcuseRequest
        fields = ['id', 'student', 'student_name', 'course', 'course_name',
                  'start_date', 'end_date', 'reason', 'supporting_document',
                  'status', 'reviewed_by', 'reviewed_by_name', 'review_comments',
                  'created_at', 'updated_at']

    def get_student_name(self, obj):
        return obj.student.user.get_full_name()

    def get_course_name(self, obj):
        return f"{obj.course.course_code} - {obj.course.course_name}"

    def get_reviewed_by_name(self, obj):
        return obj.reviewed_by.user.get_full_name() if obj.reviewed_by else None


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'title', 'message', 'is_read', 'created_at']
