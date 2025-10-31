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
)


@api_view(["GET", "POST"])
@jwt_required
@permission_classes([IsAuthenticated, ])
def task_list(request):
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
@permission_classes([IsAuthenticated, IsOwnerOrAssignerOrAdmin, ])
def task_detail(request, pk):
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
@permission_classes([IsAuthenticated, IsOwnerOrAdminOrReadOnly,])
def news_list(request):
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
@permission_classes([IsAuthenticated, IsOwnerOrAdminOrReadOnly,])
def news_detail(request, pk):
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
