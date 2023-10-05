from django.contrib import admin
from .models import Employee

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'department', 'hire_date', 'photo')
    list_display_links = ('id', 'department')
    search_fields = ('department',)
    list_per_page = 25


admin.site.register(Employee,EmployeeAdmin)
