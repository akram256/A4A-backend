from rest_framework.permissions import BasePermission


class IsProvider(BasePermission):
    """Grants Providers full access"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'PROVIDER'

class IsUser(BasePermission):
    """Grants users full access"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'USER'


class IsProfileOwner(BasePermission):
    """allow only profile owners to update profiles"""

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user