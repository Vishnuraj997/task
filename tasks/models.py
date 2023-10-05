from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from employees.models import Employee


class Task(models.Model):
    task = models.TextField(blank=True)
    assigned_by = models.CharField(max_length=50)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    department = models.CharField(max_length=100)
    task_priority = models.CharField(max_length=50)
    task_status = models.CharField(max_length=50)
    date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return f"{self.task}"
