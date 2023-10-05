
from django.contrib import admin
from rest_framework.authtoken import views
from django.urls import path,include
from tasks.views import *
from employees.views import *

urlpatterns = [

    path('register/',RegisterEmployee.as_view()),
    path('api-token-auth/', views.obtain_auth_token),
    # path('employees/',EmployeeDetails.as_view()),
    path('login/',LoginEmployee.as_view()),
    path('logout/',LogoutView.as_view()),
    path('employee/',EmployeeView.as_view()),
    path('admin/',AdminView.as_view()),
    path('task-assign/',TaskAssignView.as_view()),
    path('task-update/<str:pk>/',UpdateTask.as_view()),
    path('task-delete/<str:pk>/',DeleteTask.as_view()),
    path('admin/task-details/',TaskDetailsAdminView.as_view()),
    path('task-details/',TaskDetailsEmployeeView.as_view()),
    path('admin/', admin.site.urls),
]
