from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Employee
from tasks.models import Task


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'is_superuser']

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class EmployeeSerializer(serializers.ModelSerializer):
    employee = serializers.StringRelatedField()

    class Meta:
        model = Employee
        fields = ['id', 'employee', 'department', 'hire_date']


class TaskSerializer(serializers.ModelSerializer):
    # assigned_to = serializers.StringRelatedField()
    class Meta:
        model = Task
        fields = ['id', 'task', 'assigned_by', 'assigned_to', 'department', 'task_priority', 'task_status']
