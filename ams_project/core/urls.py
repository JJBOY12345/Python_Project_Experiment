
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView, UserViewSet, StudentViewSet, FacultyViewSet, 
    CourseViewSet, CourseStudentViewSet, AttendanceRecordViewSet,
    AttendanceCorrectionRequestViewSet, ExcuseRequestViewSet, NotificationViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'students', StudentViewSet)
router.register(r'faculty', FacultyViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'enrollments', CourseStudentViewSet)
router.register(r'attendance', AttendanceRecordViewSet)
router.register(r'correction-requests', AttendanceCorrectionRequestViewSet)
router.register(r'excuse-requests', ExcuseRequestViewSet)
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]