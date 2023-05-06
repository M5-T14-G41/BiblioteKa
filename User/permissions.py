from rest_framework import permissions
from .models import User

from rest_framework.views import Request, View

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class UserAutentication(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: User):
        if request.method in permissions.SAFE_METHODS:
            return request.user == obj or request.user.is_superuser

        if request.user != obj:
            return request.user.is_employee
        else:
            return request.user == obj


# verify if is admin if not then read only
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        return (request.method in SAFE_METHODS
                or request.user.is_employee)


# veirfy if user is authenticated
class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        return bool(request.user.is_authenticated)


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        return (request.user.is_authenticated and request.user.is_employee)
