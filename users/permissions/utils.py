from django.contrib.auth import get_user_model

User = get_user_model()


def check_owner_permission(user, obj):
    """Проверяет, что пользователь - владелец объекта"""
    return hasattr(obj, 'created_by') and obj.created_by == user


def check_assigner_permission(user, obj):
    """Проверяет, что пользователь - исполнитель объекта"""
    return hasattr(obj, 'assigned_to') and obj.assigned_to is not None and obj.assigned_to == user


def check_admin_permission(user):
    if not user:
        return False
    return user.is_admin()


def check_permissions_for_object(request, permissions, obj=None):
    """Проверяет список permissions для запроса и объекта"""
    for permission in permissions:
        if not permission.has_permission(request, None):
            return False
        if obj and hasattr(permission, 'has_object_permission'):
            if not permission.has_object_permission(request, None, obj):
                return False
    return True
