from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='admin_home'),
    path('department/add/', views.department_create, name='department_create'),
    path('department/edit/<int:id>/', views.department_edit, name='department_edit'),
    path('department/delete/<int:id>/', views.department_delete, name='department_delete'),
    path('student/add/', views.student_create, name='student_create'),
    path('student/edit/<int:id>/', views.student_edit, name='student_edit'),
    path('student/delete/<int:id>/', views.student_delete, name='student_delete'),
]
