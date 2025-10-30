from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import TokenBlacklist

User = get_user_model()


def generate_access_token(user):
    """
    Генерирует JWT access токен для пользователя.
    """
    payload = {
        "user_id": user.id,
        "email": user.email,
        "exp": datetime.utcnow() + timedelta(minutes=60),
        "iat": datetime.utcnow(),
        "type": "access"
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token


def verify_access_token(token):
    """
    Проверяет JWT токен и возвращает payload если валиден.
    """
    try:
        if TokenBlacklist.is_token_blacklisted(token):
            return None
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None

def get_user_from_token(token):
    """
    Извлекает пользователя из JWT токена.
    Возвращает пользователя или None.
    """
    payload = verify_access_token(token)
    if not payload:
        return None
    if payload.get('type') != 'access':
        return None
    try:
        user = User.objects.get(id=payload['user_id'], is_active=True)
        return user
    except User.DoesNotExist:
        return None


def extract_token_from_header(request):
    """
    Извлекает JWT токен из HTTP запроса.
    """
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        return auth_header[7:]
    return None
