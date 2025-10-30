from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserLoginSerializer(serializers.Serializer):
    """
    Сериализатор только для входа пользователя
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if not email or not password:
            raise serializers.ValidationError("Email и пароль обязательны")
        return attrs


class TokenResponseSerializer(serializers.Serializer):
    """
    Сериализатор для ответа с токеном
    """
    token = serializers.CharField()


class UserBasicSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор пользователя для auth приложения
    Только основные поля для аутентификации
    """
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'full_name']
        read_only_fields = ['id', 'email', 'first_name', 'last_name', 'full_name']