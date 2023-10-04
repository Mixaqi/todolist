from __future__ import annotations

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add, name="add"),
    path("update/<int:todo_id>/", views.update, name="update"),
    path("delete/<int:todo_id>/", views.delete, name="delete"),
    path("export_csv", views.export_csv, name = "export_csv")
]
