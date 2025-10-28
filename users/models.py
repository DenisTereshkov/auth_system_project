from django.db import models
from django.contrib.auth.models import  AbstractBaseUser, BaseUserManager

from .constants import (
    EMAIL_LENGTH,
    MAX_NAMING_LENGTH,
    MIN_NAMING_LENGTH,
)


class ProjectUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        """
        Создает и возвращает пользователя.
        """
        required_fields = {
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
        }
        missing = [field for field, value in required_fields.items() if not value]
        if missing:
            raise ValueError(f"Обязательное поле отсутствует: {missing}")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Создает и возвращает суперпользователя.
        """


class ProjectUser(AbstractBaseUser):
    """
    Кастомная модель пользователя для системы аутентификации.
    """
    email = models.EmailField(
        unique=True,
        verbose_name="Email/Почта",
        max_length=EMAIL_LENGTH,
        blank=False,
        null=False,
    )
    first_name = models.CharField(
        max_length=MAX_NAMING_LENGTH,
        verbose_name='Имя',
        blank=False,
        null=False,
    )
    last_name = models.CharField(
        max_length=MAX_NAMING_LENGTH,
        verbose_name='Фамилия',
        blank=False,
        null=False,
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    objects = ProjectUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = (
            "first_name",
            "last_name",
            "email",
        )

    def __str__(self):
        return f"{self.email} ({self.full_name})"

    @property
    def full_name(self):
        """
        Возвращает полное имя пользователя.
        """
        return ' '.join([self.last_name, self.first_name])

    def soft_delete(self):
        self.is_active = False
        self.save(update_fields=['is_active', 'updated_at'])


class Role(models.Model):
    """
    Модель ролей пользователей.
    """
    name = models.CharField(
        max_length=MAX_NAMING_LENGTH,
        unique=True,
        verbose_name='Название роли'
    )
    description = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Описание роли'
        )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'
        ordering = ['name']

    def __str__(self):
        return self.name


class UserRole(models.Model):
    """
    Связь многие-ко-многим пользователей и ролей.
    """
    user = models.ForeignKey(
        ProjectUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        verbose_name='Роль'
    )

    class Meta:
        verbose_name = 'Роль пользователя'
        verbose_name_plural = 'Роли пользователей'
        unique_together = ['user', 'role']
        ordering = ['user']

    def __str__(self):
        return f"{self.user.email} - {self.role.name}"
