from rest_framework import permissions
from .utils import (
    check_owner_permission as owner,
    check_assigner_permission as assigner, 
    check_admin_permission as admin
)


class IsAuthenticated(permissions.BasePermission):
    """Только аутентифицированные пользователи"""
    def has_permission(self, request, view):
        return hasattr(request, 'user') and request.user is not None
    

class IsOwnerOrAdmin(permissions.BasePermission):
    """Разрешает доступ только владельцу объекта или админу"""
    
    def has_object_permission(self, request, view, obj):
        return owner(request.user, obj) or admin(request.user)

class IsAssignerOrAdmin(permissions.BasePermission):
    """Разрешает доступ только исполнителю или админу"""
    
    def has_object_permission(self, request, view, obj):
        return assigner(request.user, obj) or admin(request.user)

class IsOwnerOrAssignerOrAdmin(permissions.BasePermission):
    """Разрешает доступ владельцу, исполнителю или админу"""
    
    def has_object_permission(self, request, view, obj):
        return owner(request.user, obj) or assigner(request.user, obj) or admin(request.user)

class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешает:
    - GET, HEAD, OPTIONS всем аутентифицированным  
    - PUT, PATCH, DELETE только владельцу или админу
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return owner(request.user, obj) or admin(request.user)

class IsAdmin(permissions.BasePermission):
    """Только для админов"""
    def has_permission(self, request, view):
        return admin(request.user)