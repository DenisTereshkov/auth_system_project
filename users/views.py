from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from app_auth.decorators import jwt_required
from .serializers import (
    UserRegisterSerializer,
    UserPrivateSerializer,
    UserUpdateSerializer
    )

User = get_user_model()


@api_view(['POST'])
def register(request):
    """
    Регистрация нового пользователя.
    POST /api/users/register/
    """
    input_serializer = UserRegisterSerializer(data=request.data)

    if input_serializer.is_valid():
        user = input_serializer.save()
        user_serializer = UserPrivateSerializer(user)
        return Response({
            'message': 'Пользователь успешно создан',
            'data': user_serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response({
        'error': 'Ошибка валидации',
        'details': input_serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@jwt_required
def profile(request):
    """
    Получить профиль пользователя.
    GET /api/users/profile/
    """
    serializer = UserPrivateSerializer(request.user)
    return Response({
        'data': serializer.data
    })


@api_view(['PUT'])
@jwt_required
def update_profile(request):
    """
    Обновить профиль пользователя.
    PUT /api/users/profile/
    """
    input_serializer = UserUpdateSerializer(
        request.user,
        data=request.data,
        partial=True
    )
    if input_serializer.is_valid():
        user = input_serializer.save()
        response_serializer = UserPrivateSerializer(user)
        return Response({
            'message': 'Профиль обновлен',
            'data': response_serializer.data
        })
    return Response({
        'error': 'Ошибка валидации',
        'details': input_serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@jwt_required
def delete_account(request):
    """
    Мягкое удаление аккаунта.
    DELETE /api/users/delete-account/
    """
    request.user.soft_delete()
    return Response({
        'message': 'Аккаунт успешно удален'
    })
