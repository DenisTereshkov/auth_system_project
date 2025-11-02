from django.urls import path
from . import views

urlpatterns = [
    path('news/', views.news_list, name='news-list'),
    path('news/<int:pk>/', views.news_detail, name='news-detail'),
    path('tasks/', views.task_list, name='task-list'),
    path('tasks/<int:pk>/', views.task_detail, name='task-detail'),
    path(
        'tasks/owner-or-admin/<int:task_id>/',
        views.simple_owner_or_admin,
        name='simple_owner_or_admin'
        ),
    path(
        'tasks/assigner-or-admin/<int:task_id>/',
        views.simple_assigner_or_admin,
        name='simple_assigner_or_admin'

    ),
    path(
        'tasks/admin-only/',
        views.simple_admin_only,
        name='simple_admin_only'
    ),
]
