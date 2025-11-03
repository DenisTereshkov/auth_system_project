from rest_framework import serializers

from .models import Task, News


class TaskSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(
        source="created_by.full_name",
        read_only=True
    )
    assigned_to_name = serializers.CharField(
        source="assigned_to.full_name",
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ["id", "created_by", "created_at", "updated_at"]


class NewsSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(
        source="created_by.full_name",
        read_only=True
    )

    class Meta:
        model = News
        fields = "__all__"
        read_only_fields = ["id", "created_by", "created_at", "updated_at"]
