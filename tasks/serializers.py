from rest_framework import serializers
from .models import Task, ActivityLog

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['user']

class ActivityLogSerializer(serializers.ModelSerializer):
    task_title = serializers.CharField(source='task.title', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = ActivityLog
        fields = [
            "id",
            "task",
            "task_title",
            "user",
            "user_name",
            "action",
            "old_value",
            "new_value",
            "timestamp"
        ]
