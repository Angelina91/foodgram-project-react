from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Или пользователь является админом,
    или можно только посмотреть
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.user.is_admin
                or request.method in permissions.SAFE_METHODS
            )
        return request.method in permissions.SAFE_METHODS


class IsAuthorOrReadOnly(permissions.BasePermission):
    "Право только у автора контента"

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
