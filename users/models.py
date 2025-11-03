from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

from .constants import (
    EMAIL_LENGTH,
    MAX_NAMING_LENGTH,
)


class RoleType(models.TextChoices):
    USER = "user", "Обычный пользователь"
    ADMIN = "admin", "Администратор"
    SUPERUSER = "superuser", "Суперпользователь"


class ProjectUserManager(BaseUserManager):
    def create_user(
        self, email, first_name, last_name,
        password=None, role=RoleType.USER
    ):
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=role
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        return self.create_user(
            email=email,
            password=password,
            first_name=extra_fields.get('first_name', 'Admin'),
            last_name=extra_fields.get('last_name', 'Admin'),
            role=RoleType.SUPERUSER
        )


class ProjectUser(AbstractBaseUser):
    email = models.EmailField(
        max_length=EMAIL_LENGTH,
        unique=True,
        verbose_name="Email/Почта"
    )
    first_name = models.CharField(
        max_length=MAX_NAMING_LENGTH,
        verbose_name="Имя"
    )
    last_name = models.CharField(
        max_length=MAX_NAMING_LENGTH,
        verbose_name="Фамилия"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен"
    )
    role = models.CharField(
        max_length=20,
        choices=RoleType.choices,
        default=RoleType.USER,
        verbose_name="Роль"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ProjectUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.email} ({self.full_name})"

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name}"

    def soft_delete(self):
        self.is_active = False
        self.save()

    def is_admin(self):
        return self.role in [RoleType.ADMIN, RoleType.SUPERUSER]

    def is_superuser(self):
        return self.role == RoleType.SUPERUSER

    def is_regular_user(self):
        return self.role == RoleType.USER
