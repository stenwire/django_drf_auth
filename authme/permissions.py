from rest_framework.permissions import BasePermission


class IsAdminUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ["POST", "PUT", "DELETE"]:
            return request.user.is_superuser
        return True


class ProtectAllMethods(BasePermission):
    def has_permission(self, request, view):
        if request.method in ["GET", "POST", "PUT", "DELETE"]:
            return request.user.is_superuser
        return True
