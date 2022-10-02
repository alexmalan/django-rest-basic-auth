from rest_framework import permissions


class IsSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "SELLER"


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.id == view.get_object().user_id.id


class IsBuyer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "BUYER"
