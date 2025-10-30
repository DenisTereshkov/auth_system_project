from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from .utils import get_user_from_token


def jwt_required(view_func):
    """
    Декоратор для JWT аутентификации.
    Проверяет наличие и валидность JWT токена.
    """
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return Response(
                {
                    'error': 'Требуется аутентификация',
                    'message': 'Отсутствует JWT токен. Используйте формат: Authorization: Bearer <token>'
                }, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        token = auth_header[7:].strip()
        if not token:
            return Response(
                {
                    'error': 'Невалидный токен',
                    'message': 'Токен не может быть пустым'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        user = get_user_from_token(token)
        if not user:
            return Response(
                {
                    'error': 'Невалидный токен',
                    'message': 'Токен невалиден, просрочен или пользователь неактивен'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        request.user = user
        return view_func(request, *args, **kwargs)
    return wrapped_view
