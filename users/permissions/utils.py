from django.contrib.auth import get_user_model

User = get_user_model()


def check_owner_permission(user, obj):
    """Проверяет, что пользователь - владелец объекта"""
    return hasattr(obj, 'created_by') and obj.created_by == user


def check_admin_permission(user):
    return user and user.is_authenticated and user.is_admin()
