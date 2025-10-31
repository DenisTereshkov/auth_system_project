from django.contrib.auth import get_user_model

User = get_user_model()


def check_owner_permission(user, obj):
    """Проверяет, что пользователь - владелец объекта"""
    return hasattr(obj, 'created_by') and obj.created_by == user


def check_admin_permission(user):
    """Проверяет, что пользователь - админ"""
    if not user or not user.is_authenticated:
        return False
    return user.userrole_set.filter(role__name="admin").exists()
