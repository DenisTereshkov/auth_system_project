from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()


class UserPublicSerializer(serializers.ModelSerializer):
    """
    Сериализатор для публичных данных.
    Минимальный набор полей для идентификации пользователя.
    """
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'full_name']
        read_only_fields = fields


class UserPrivateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для приватных данных пользователя (профиль).
    """
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 
                 'full_name', 'role', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'email', 'role', 'is_active', 'created_at', 'updated_at']


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Сериализатор только для регистрации.
    """
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirm', 'first_name', 'last_name']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует")
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password_confirm'):
            raise serializers.ValidationError({"password_confirm": "Пароли не совпадают"})
        return attrs
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор только для обновления профиля
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
