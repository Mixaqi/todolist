from __future__ import annotations

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("todolist.urls")),
    path("accounts", include("django.contrib.auth.urls")),
]
