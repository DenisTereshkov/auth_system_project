from django.urls import path

from .views import (
    news_list,
    news_detail,
    task_list,
    task_detail,
    simple_owner_or_admin,
    simple_assigner_or_admin,
    simple_admin_only,
)

urlpatterns = [
    path('news/', news_list, name='news-list'),
    path('news/<int:pk>/', news_detail, name='news-detail'),
    path('tasks/', task_list, name='task-list'),
    path('tasks/<int:pk>/', task_detail, name='task-detail'),
    path(
        'tasks/owner-or-admin/<int:task_id>/',
        simple_owner_or_admin,
        name='simple_owner_or_admin',
    ),
    path(
        'tasks/assigner-or-admin/<int:task_id>/',
        simple_assigner_or_admin,
        name='simple_assigner_or_admin',
    ),
    path(
        'tasks/admin-only/',
        simple_admin_only,
        name='simple_admin_only',
    ),
]
