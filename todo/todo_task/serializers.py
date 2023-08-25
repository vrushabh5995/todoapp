from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["task_id", "task_title", "task_discription", "task_status","task_due_date","updated_at"]
