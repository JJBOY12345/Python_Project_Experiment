# core/permissions.py

from rest_framework import permissions
from django.contrib.auth import get_user_model

User = get_user_model()

class IsAdminUser(permissions.BasePermission):
    """
    Permission to only allow admin users to access the view.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.ADMIN

class IsFacultyUser(permissions.BasePermission):
    """
    Permission to only allow faculty users to access the view.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.FACULTY

class IsStudentUser(permissions.BasePermission):
    """
    Permission to only allow student users to access the view.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.STUDENT

class IsOwner(permissions.BasePermission):
    """
    Permission to only allow owners of an object to access it.
    """
    def has_object_permission(self, request, view, obj):
        # Instance must have an attribute named `user` or `owner`
        if hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'owner'):
            return obj.owner == request.user
        return False