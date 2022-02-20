from rest_framework import permissions
from rest_framework.exceptions import MethodNotAllowed


class GroupPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method not in permissions.SAFE_METHODS:
            raise MethodNotAllowed(request.method)
        # return request.method in permissions.SAFE_METHODS - этот код
        # работает, но выбрасывает исключение 403, а тесты требуют - 405.
        # Поэтому я оставил свой старый код.
        return True


class PostCommentPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        list_method = ['PUT', 'PATCH', 'DELETE']
        if request.method in list_method:
            return obj.author == request.user
        return True
