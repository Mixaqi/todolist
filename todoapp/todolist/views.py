from __future__ import annotations

from typing import TYPE_CHECKING

from django.shortcuts import render

from .models import ToDo

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


def index(request: HttpRequest) -> HttpResponse:
    todos = ToDo.objects.all()
    return render(
        request,
        "todoapp/index.html",
        {"todo_list": todos, "title": "Главная страница"},
    )
