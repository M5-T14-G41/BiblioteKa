from rest_framework import permissions
from .models import User


class UserAutentication(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: User):
        if request.method in permissions.SAFE_METHODS:
            return request.user == obj or request.user.is_superuser

        if request.user != obj:
            return request.user.is_employee
        else:
            return request.user == obj
