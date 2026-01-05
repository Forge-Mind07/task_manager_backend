from rest_framework import generics
from .models import Task, ActivityLog
from .serializers import TaskSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from .serializers import ActivityLogSerializer




class TaskListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    queryset = Task.objects.select_related('user').all()

    filter_backends = [DjangoFilterBackend, OrderingFilter]

    # Filters
    filterset_fields = {
        'status': ['exact'],
        'priority': ['exact'],
        'due_date': ['gte', 'lte'],
        'created_at': ['gte', 'lte']
    }

    # Sorting
    ordering_fields = ['due_date', 'priority', 'created_at']

    def get_queryset(self):
        user = self.request.user

        # ADMIN = see all
        if user.is_superuser:
            return Task.objects.select_related('user').all()

        # INTERN = only own tasks
        return Task.objects.select_related('user').filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    queryset = Task.objects.select_related('user').all()

    def get_queryset(self):
        user = self.request.user
        
        if user.is_superuser:
            return Task.objects.select_related('user').all()

        return Task.objects.select_related('user').filter(user=user)
    

from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

class TaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        task = super().get_object()
        user = self.request.user

        # Admin full access
        if user.is_superuser:
            return task
        
        # Normal user — only own tasks
        if task.user != user:
            raise PermissionDenied("You are not allowed to access this task")

        return task
    def perform_update(self, serializer):
        task = self.get_object()
        user = self.request.user

        old_status = task.status
        old_data = TaskSerializer(task).data

        updated_task = serializer.save()

        new_status = updated_task.status
        new_data = TaskSerializer(updated_task).data

    # General Update Log
        ActivityLog.objects.create(
        task=task,
        user=user,
        action="UPDATED",
        old_value=str(old_data),
        new_value=str(new_data)
    )

    # Status Change Log
        if old_status != new_status:
            ActivityLog.objects.create(
                task=task,
                user=user,
                action="STATUS_CHANGED",
                old_value=old_status,
                new_value=new_status
                )

    # Delete activity log        
    def perform_destroy(self, instance):
        ActivityLog.objects.create(
            task=instance,
            user=self.request.user,
            action="DELETED",
            old_value=instance.status,
            new_value=None
            )
        instance.delete()

class ActivityLogListAPIView(generics.ListAPIView):
    queryset = ActivityLog.objects.select_related("task", "user").order_by("-timestamp")
    serializer_class = ActivityLogSerializer
    permission_classes = [IsAuthenticated]



    




