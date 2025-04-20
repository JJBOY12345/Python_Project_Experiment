# core/views.py

from rest_framework import viewsets, status, generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import (
    Student, Faculty, Course, CourseStudent, 
    AttendanceRecord, AttendanceCorrectionRequest, 
    ExcuseRequest, Notification
)
from .serializers import (
    UserSerializer, RegisterSerializer, StudentSerializer, FacultySerializer,
    CourseSerializer, CourseStudentSerializer, AttendanceRecordSerializer,
    AttendanceCorrectionRequestSerializer, ExcuseRequestSerializer, NotificationSerializer
)

User = get_user_model()

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.ADMIN

class IsFacultyUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.FACULTY

class IsStudentUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.STUDENT

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        return [IsAuthenticated()]

class FacultyViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        return [IsAuthenticated()]

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), (IsAdminUser() | IsFacultyUser())]
        return [IsAuthenticated()]
    
    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        course = self.get_object()
        enrollments = CourseStudent.objects.filter(course=course)
        serializer = CourseStudentSerializer(enrollments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def attendance(self, request, pk=None):
        course = self.get_object()
        records = AttendanceRecord.objects.filter(course=course)
        serializer = AttendanceRecordSerializer(records, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='teaching')
    def teaching_courses(self, request):
        """Return courses taught by the logged-in faculty."""
        if not hasattr(request.user, 'faculty_profile'):
            return Response({"error": "Only faculty can view this"}, status=status.HTTP_403_FORBIDDEN)

        faculty = request.user.faculty_profile
        courses = Course.objects.filter(faculty=faculty)
        serializer = self.get_serializer(courses, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='teaching', permission_classes=[IsAuthenticated, IsFacultyUser])
    def get_teaching_courses(self, request):
        """Return the list of courses the faculty is teaching"""
        faculty = request.user.faculty_profile
        courses = Course.objects.filter(faculty=faculty).values('id', 'course_code', 'course_name')
        return Response(courses, status=status.HTTP_200_OK)


class CourseStudentViewSet(viewsets.ModelViewSet):
    queryset = CourseStudent.objects.all()
    serializer_class = CourseStudentSerializer
    permission_classes = [IsAuthenticated, (IsAdminUser | IsFacultyUser)]

class AttendanceRecordViewSet(viewsets.ModelViewSet):
    queryset = AttendanceRecord.objects.all()
    serializer_class = AttendanceRecordSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), (IsAdminUser() | IsFacultyUser())]
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        if hasattr(self.request.user, 'faculty_profile'):
            serializer.save(marked_by=self.request.user.faculty_profile)
        else:
            serializer.save()
    
    @action(detail=False, methods=['get'])
    def my_attendance(self, request):
        if not hasattr(request.user, 'student_profile'):
            return Response(
                {"error": "Only students can view their attendance"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        records = AttendanceRecord.objects.filter(student=request.user.student_profile)
        serializer = self.get_serializer(records, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], url_path='batch_mark', permission_classes=[IsAuthenticated, IsFacultyUser])
    def batch_mark(self, request):
        """Handle batch marking of attendance records"""
        course_id = request.data.get('course_id')
        date = request.data.get('date')
        records = request.data.get('records', [])

        if not course_id or not date or not records:
            return Response(
                {"error": "course_id, date, and records are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        course = get_object_or_404(Course, id=course_id)
        faculty = request.user.faculty_profile

        if course.faculty != faculty:
            return Response(
                {"error": "You are not authorized to mark attendance for this course."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Create attendance records
        created_records = []
        for record in records:
            student_id = record.get('student')
            status_value = record.get('status', 'absent')
            student = get_object_or_404(Student, id=student_id)

            attendance_record, created = AttendanceRecord.objects.update_or_create(
                course=course,
                student=student,
                date=date,
                defaults={'status': status_value, 'marked_by': faculty}
            )
            created_records.append(attendance_record)

        return Response(
            {"success": True, "message": "Attendance marked successfully."},
            status=status.HTTP_200_OK
        )


class AttendanceCorrectionRequestViewSet(viewsets.ModelViewSet):
    queryset = AttendanceCorrectionRequest.objects.all()
    serializer_class = AttendanceCorrectionRequestSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create']:
            return [IsAuthenticated(), IsStudentUser()]
        elif self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), (IsAdminUser() | IsFacultyUser())]
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        if hasattr(self.request.user, 'student_profile'):
            serializer.save(requested_by=self.request.user.student_profile)
        else:
            serializer.save()
    
    def perform_update(self, serializer):
        if hasattr(self.request.user, 'faculty_profile'):
            serializer.save(reviewed_by=self.request.user.faculty_profile)
        else:
            serializer.save()
    
    @action(detail=False, methods=['get'])
    def my_requests(self, request):
        if not hasattr(request.user, 'student_profile'):
            return Response(
                {"error": "Only students can view their correction requests"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        requests = AttendanceCorrectionRequest.objects.filter(requested_by=request.user.student_profile)
        serializer = self.get_serializer(requests, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pending_reviews(self, request):
        if not hasattr(request.user, 'faculty_profile'):
            return Response(
                {"error": "Only faculty can view pending reviews"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get pending requests for courses taught by this faculty
        faculty_courses = Course.objects.filter(faculty=request.user.faculty_profile)
        pending_requests = AttendanceCorrectionRequest.objects.filter(
            status='pending',
            attendance_record__course__in=faculty_courses
        )
        serializer = self.get_serializer(pending_requests, many=True)
        return Response(serializer.data)

class ExcuseRequestViewSet(viewsets.ModelViewSet):
    queryset = ExcuseRequest.objects.all()
    serializer_class = ExcuseRequestSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create']:
            return [IsAuthenticated(), IsStudentUser()]
        elif self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), (IsAdminUser() | IsFacultyUser())]
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        if hasattr(self.request.user, 'student_profile'):
            serializer.save(student=self.request.user.student_profile)
        else:
            serializer.save()
    
    def perform_update(self, serializer):
        if hasattr(self.request.user, 'faculty_profile'):
            serializer.save(reviewed_by=self.request.user.faculty_profile)
        else:
            serializer.save()
    
    @action(detail=False, methods=['get'])
    def my_requests(self, request):
        if not hasattr(request.user, 'student_profile'):
            return Response(
                {"error": "Only students can view their excuse requests"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        requests = ExcuseRequest.objects.filter(student=request.user.student_profile)
        serializer = self.get_serializer(requests, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pending_reviews(self, request):
        if not hasattr(request.user, 'faculty_profile'):
            return Response(
                {"error": "Only faculty can view pending reviews"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get pending requests for courses taught by this faculty
        faculty_courses = Course.objects.filter(faculty=request.user.faculty_profile)
        pending_requests = ExcuseRequest.objects.filter(
            status='pending',
            course__in=faculty_courses
        )
        serializer = self.get_serializer(pending_requests, many=True)
        return Response(serializer.data)

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        notifications = self.get_queryset().filter(is_read=False)
        notifications.update(is_read=True)
        return Response({"status": "All notifications marked as read"})
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({"status": "Notification marked as read"})