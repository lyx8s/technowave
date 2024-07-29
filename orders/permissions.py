from rest_framework import permissions


class IsCurrentUserOrAccessIsDenied(permissions.IsAuthenticatedOrReadOnly):
    """
    Разрешение на действия только от владельца корзины
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
