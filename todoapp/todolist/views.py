from __future__ import annotations

from typing import TYPE_CHECKING
import datetime

from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse

from .models import ToDo
import csv
import datetime

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
    todo = ToDo.objects.get(id=todo_id)
    todo.delete()
    return redirect("index")


# def export_csv(request) -> HttpResponse:
#     response = HttpResponse(content_type="text/csv")
#     timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#     response["Content-Disposition"] = f"attachment; filename=my_todolist_{timestamp}.csv"
#     writer = csv.writer(response)
#     writer.writerow(["title", "is_complete"])
#     affairs = ToDo.objects.filter(owner=request.user)
#     for affair in affairs:
#         writer.writerow([affair.title, affair.is_complete])
#     return response

def export_csv(request) -> HttpResponse:
    response = HttpResponse(content_type="text/csv")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    response["Content-Disposition"] = f"attachment; filename=my_todolist_{timestamp}.csv"
    writer = csv.writer(response)
    writer.writerow(["title", "is_complete"])
    affairs = ToDo.objects.all()  # Убрано условие фильтрации по owner
    for affair in affairs:
        writer.writerow([affair.title, affair.is_complete])
    return response
