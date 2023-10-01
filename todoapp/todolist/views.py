from __future__ import annotations

from typing import TYPE_CHECKING

from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

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


@require_http_methods(["POST"])
def add(request: HttpRequest) -> HttpResponse:
    title = request.POST["title"]
    todo = ToDo(title=title)
    todo.save()
    return redirect("index")


def update(request: HttpRequest, todo_id: int) -> HttpResponse:
    todo = ToDo.objects.get(id=todo_id)
    todo.is_complete = not todo.is_complete
    todo.save()
    return redirect("index")

def delete(request: HttpRequest, todo_id: int) -> HttpResponse:
    todo = ToDo.objects.get(id = todo_id)
    todo.delete()
    return redirect("index")
