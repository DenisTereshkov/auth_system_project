from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Entities(models.Model):
    """Базовая модель сущности."""
    title = models.CharField(max_length=200, verbose_name="Название сущности")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Task(Entities):
    """Демонстрационная модель задачи."""
    STATUS_CHOICES = [
        ("pending", "Ожидает"),
        ("completed", "Выполнено"),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Название задачи")
    description = models.TextField(blank=True, verbose_name="Описание")
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_tasks",
        verbose_name="Кто создал"
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tasks",
        verbose_name="Кто выполняет"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name="Статус"
    )

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ["-created_at"]


class News(Entities):
    """Демонстрационная модель новости."""
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Текст новости")
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_news",
        verbose_name="Кто создал"
    )

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ["-created_at"]
