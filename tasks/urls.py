from django.urls import path

from .views import TaskListCreateAPIView, TaskDetailAPIView, ActivityLogListAPIView

urlpatterns = [
    path('tasks/', TaskListCreateAPIView.as_view()),
    path('tasks/<int:pk>/', TaskDetailAPIView.as_view()),
    path("tasks/logs/", ActivityLogListAPIView.as_view(), name="task-logs"),

]
