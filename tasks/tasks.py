from celery import shared_task
from django.utils import timezone
from .models import Task, ActivityLog

@shared_task(name="tasks.tasks_celery.mark_overdue_tasks")
def mark_overdue_tasks():
    now = timezone.now().date()

    overdue_tasks = Task.objects.filter(
        due_date__lt=now,
        status__in=["PENDING", "IN_PROGRESS"]
    )

    for task in overdue_tasks:
        old_value = task.status
        task.status = "OVERDUE"
        task.save()

        ActivityLog.objects.create(
            task=task,
            user=task.user,
            action="STATUS_CHANGED",
            old_value=old_value,
            new_value="OVERDUE"
        )

    return f"{overdue_tasks.count()} tasks marked overdue"
