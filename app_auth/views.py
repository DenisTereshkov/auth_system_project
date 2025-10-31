from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from .utils import generate_access_token
from .decorators import jwt_required
from .serializers import UserLoginSerializer, TokenResponseSerializer
from .models import TokenBlacklist

User = get_user_model()


@api_view(['POST'])
def login(request):
    """
    Аутентификация пользователя
    POST /api/auth/login/
    """
    input_serializer = UserLoginSerializer(data=request.data)
    if not input_serializer.is_valid():
        return Response(
            {
                'error': 'Ошибка валидации',
                'details': input_serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    email = input_serializer.validated_data['email']
    password = input_serializer.validated_data['password']
    try:
        user = User.objects.get(email=email, is_active=True)
        if not check_password(password, user.password):
            return Response(
                {'error': 'Неверный email или пароль'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        token = generate_access_token(user)
        response_serializer = TokenResponseSerializer({
            'token': token,
        })
        return Response(response_serializer.data)
    except User.DoesNotExist:
        return Response(
            {'error': 'Неверный email или пароль'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@jwt_required
def logout(request):
    """
    Выход из системы
    POST /api/auth/logout/
    """
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    TokenBlacklist.add_token(token, request.user, reason='logout')
    return Response({
        'message': 'Успешный выход из системы'
    })
