from __future__ import annotations

from django.contrib import admin

from .models import ToDo

admin.site.register(ToDo)
