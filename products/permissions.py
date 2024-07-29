from rest_framework import permissions


class IsAdminOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """Разрешение только для автора или только на чтение."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or
            bool(request.user and request.user.is_staff)
        )
