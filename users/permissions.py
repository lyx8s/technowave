from rest_framework import permissions


class IsAdminOrReadOnly(permissions.IsAuthenticated):
    """Разрешение только для автора или только на чтение."""

    def has_permission(self, request, view):
        return (
            bool(request.user and request.user.is_staff)
        )