from __future__ import annotations

from django.contrib import admin

from .models import ToDo, AttachedFile

admin.site.register(ToDo)
admin.site.register(AttachedFile)
