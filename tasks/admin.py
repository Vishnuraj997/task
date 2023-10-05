from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'assigned_by', 'assigned_to', 'department', 'task_priority', 'task_status')
    list_display_links = ('id', 'task', 'assigned_by')
    search_fields = ('assigned_by',)
    list_per_page = 25


admin.site.register(Task, TaskAdmin)
