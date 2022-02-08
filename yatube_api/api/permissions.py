from rest_framework import permissions
from rest_framework.exceptions import MethodNotAllowed, PermissionDenied


class GroupPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method not in permissions.SAFE_METHODS:
            raise MethodNotAllowed(request.method)
        return True


class PostCommentPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        print(obj.author)
        list_method = ['PUT', 'PATCH', 'DELETE']
        if request.method in list_method:
            if request.user != obj.author:
                error = 'Изменение и удаление чужого контента запрещено!'
                raise PermissionDenied(error)
        return True
