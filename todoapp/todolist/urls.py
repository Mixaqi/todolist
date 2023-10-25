from __future__ import annotations

from django.urls import path

from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add, name="add"),
    path("update/<int:todo_id>/", views.update, name="update"),
    path("delete/<int:todo_id>/", views.delete, name="delete"),
    path("export_csv", views.export_csv, name = "export_csv"),
    path("export_excel", views.export_excel, name = "export_excel"),
    path("attach_file/<int:task_id>/", views.attach_file_to_task, name="attach_file_to_task")

]