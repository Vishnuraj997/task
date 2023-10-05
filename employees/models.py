from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    department = models.CharField(max_length=100)
    hire_date = models.DateTimeField(default=datetime.now, blank=True)

    @property
    def __str__(self):
        return f"{self.department}"
