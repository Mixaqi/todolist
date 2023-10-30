from __future__ import annotations

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add, name="add"),
    path("update/<int:todo_id>/", views.update, name="update"),
    path("delete/<int:todo_id>/", views.delete, name="delete"),
    path("export_csv", views.export_csv, name = "export_csv"),
    path("export_excel", views.export_excel, name = "export_excel"),
    path("attach_file/<int:task_id>/", views.attach_file_to_task, name="attach_file_to_task"),
    path("download_file/<int:file_id>/", views.download_file, name="download_file"),
    path("delete_attached_file/<int:attached_file_id>/", views.delete_attached_file, name="delete_attached_file"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
