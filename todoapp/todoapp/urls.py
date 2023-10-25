from __future__ import annotations
from django import views

from django.contrib import admin
from django.urls import include, path
from todolist import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("todolist.urls")),
    path('export_csv/', views.export_csv, name='export_csv'),
    path('attach_file_to_task/<int:task_id>/', views.attach_file_to_task, name='attach_file_to_task'),
]
