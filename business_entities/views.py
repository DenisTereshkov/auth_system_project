from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from app_auth.decorators import jwt_required
from .models import Task, News
from .serializers import TaskSerializer, NewsSerializer
from users.permissions.permissions import (
    IsAuthenticated,
    IsOwnerOrAssignerOrAdmin,
    IsOwnerOrAdminOrReadOnly,
    IsAdmin,
    IsAssignerOrAdmin,
    IsOwnerOrAdmin,
)
from users.permissions.utils import check_permissions_for_object


@api_view(["GET", "POST"])
@jwt_required
def task_list(request):
    permissions = (IsAuthenticated(),)
    if not check_permissions_for_object(request, permissions):
        return Response({
            "error": "Доступ запрещен",
            "message": "Недостаточно прав"
        }, status=403)
    if request.method == "GET":
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response({"data": serializer.data})
    elif request.method == "POST":
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response({
                "message": "Задача создана",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "error": "Ошибка валидации",
            "details": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@jwt_required
def task_detail(request, pk):
    permissions = (IsAuthenticated(), IsOwnerOrAssignerOrAdmin())
    if not check_permissions_for_object(request, permissions, pk):
        return Response({
            "error": "Доступ запрещен",
            "message": "Недостаточно прав"
        }, status=403)
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response({
            "error": "Задача не найдена"
        }, status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = TaskSerializer(task)
        return Response({"data": serializer.data})
    elif request.method == "PUT":
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Задача обновлена",
                "data": serializer.data
            })
        return Response({
            "error": "Ошибка валидации",
            "details": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        task.delete()
        return Response({
            "message": "Задача удалена"
        })


@api_view(["GET", "POST"])
@jwt_required
def news_list(request):
    permissions = (IsAuthenticated(), IsOwnerOrAdminOrReadOnly())
    if not check_permissions_for_object(request, permissions):
        return Response({
            "error": "Доступ запрещен",
            "message": "Недостаточно прав"
        }, status=403)
    if request.method == "GET":
        news = News.objects.all()
        serializer = NewsSerializer(news, many=True)
        return Response({"data": serializer.data})
    elif request.method == "POST":
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response({
                "message": "Новость создана",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "error": "Ошибка валидации",
            "details": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@jwt_required
def news_detail(request, pk):
    permissions = (IsAuthenticated(), IsOwnerOrAdminOrReadOnly())
    if not check_permissions_for_object(request, permissions, pk):
        return Response({
            "error": "Доступ запрещен",
            "message": "Недостаточно прав"
        }, status=403)
    try:
        news = News.objects.get(pk=pk)
    except News.DoesNotExist:
        return Response({
            "error": "Новость не найдена"
        }, status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = NewsSerializer(news)
        return Response({"data": serializer.data})
    elif request.method == "PUT":
        serializer = NewsSerializer(news, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Новость обновлена",
                "data": serializer.data
            })
        return Response({
            "error": "Ошибка валидации",
            "details": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        news.delete()
        return Response({
            "message": "Новость удалена"
        })


@api_view(["GET"])
@jwt_required
def simple_admin_only(request):
    """Только для админов"""
    permissions = (IsAuthenticated(), IsAdmin())
    if not check_permissions_for_object(request, permissions):
        return Response({
            "error": "Доступ запрещен",
            "message": "Недостаточно прав"
        }, status=403)
    return Response({"message": "Вы админ"})


@api_view(["GET"])
@jwt_required
def simple_owner_or_admin(request, task_id):
    """Только владелец задачи или админ"""
    permissions = (IsAuthenticated(), IsOwnerOrAdmin())
    if not check_permissions_for_object(request, permissions, task_id):
        return Response({
            "error": "Доступ запрещен",
            "message": "Недостаточно прав"
        }, status=403)
    return Response({"message": "Вы владелец задачи или админ"})


@api_view(["GET"])
@jwt_required
def simple_assigner_or_admin(request, task_id):
    """Только исполнитель задачи или админ"""
    permissions = (IsAuthenticated(), IsAssignerOrAdmin())
    if not check_permissions_for_object(request, permissions, task_id):
        return Response({
            "error": "Доступ запрещен",
            "message": "Недостаточно прав"
        }, status=403)
    return Response({"message": "Вы исполнитель задачи или админ"})