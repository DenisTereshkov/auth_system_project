from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.task_list, name='task-list'),
    path('tasks/<int:pk>/', views.task_detail, name='task-detail'),
    path('news/', views.news_list, name='news-list'),
    path('news/<int:pk>/', views.news_detail, name='news-detail'),
]
