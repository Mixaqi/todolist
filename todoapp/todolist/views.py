from __future__ import annotations

from typing import TYPE_CHECKING
import datetime
from urllib import response

from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse

from .models import ToDo
import csv
import datetime
import xlwt

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


def export_csv(request: HttpRequest) -> HttpResponse:
    response = HttpResponse(content_type="text/csv")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    response[
        "Content-Disposition"
    ] = f"attachment; filename=my_todolist_{timestamp}.csv"
    writer = csv.writer(response)
    writer.writerow(["title", "is_complete"])
    affairs = ToDo.objects.all()  # Убрано условие фильтрации по owner
    for affair in affairs:
        writer.writerow([affair.title, affair.is_complete])
    return response


def export_excel(request: HttpRequest) -> HttpResponse:
    response = HttpResponse(content_type="application/ms_excel")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    response[
        "Content-Disposition"
    ] = f"attachment; filename=my_todolist_{timestamp}.xls"
    wb = xlwt.Workbook(encoding="utf-8")
    ws = wb.add_sheet("activity")
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ["title", "is_complete"]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    todos = ToDo.objects.all()

    for todo in todos:
        row_num += 1
        ws.write(row_num, 0, todo.title, font_style)
        ws.write(row_num, 1, todo.is_complete, font_style)

    wb.save(response)
    return response
