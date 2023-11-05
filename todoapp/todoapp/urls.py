from __future__ import annotations

from django.contrib import admin
from django.urls import include, path
from todolist.views import user_login, user_logout

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("todolist.urls")),
    path("login/", user_login, name="login"),
    #path("logout/", user_logout, name="logout"),
]
