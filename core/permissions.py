from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    message = 'Permission Denied. You are not the owner of the question.'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user

    def has_object_permission(self, request, view, obj):
        return obj.author.id == request.user.id
