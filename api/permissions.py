from rest_framework import permissions


class IsLoggedInUserOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff



class IsAdminUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return True



class IsPublic(permissions.BasePermission):

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return True
