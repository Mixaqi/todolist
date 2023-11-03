from __future__ import annotations

from typing import TYPE_CHECKING
import datetime

from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from django.shortcuts import render, redirect
from .models import ToDo, AttachedFile
from .forms import AttachedFileForm
from .models import ToDo
import csv
import xlwt

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse, FileResponse


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
    if len(title) != 0:
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
    timestamp = datetime.datetime.now().strftime("%Y_%m_%d %H:%M:%S")
    response[
        "Content-Disposition"
    ] = f"attachment; filename=my_todolist_{timestamp}.csv"
    writer = csv.writer(response)
    writer.writerow(["Задание", "Готовность"])
    affairs = ToDo.objects.all()  # Убрано условие фильтрации по owner
    for affair in affairs:
        writer.writerow([affair.title, affair.is_complete])
    return response


def export_excel(request: HttpRequest) -> HttpResponse:
    response = HttpResponse(content_type="application/ms_excel")
    timestamp = datetime.datetime.now().strftime("%Y_%m_%d %H:%M:%S")
    response[
        "Content-Disposition"
    ] = f"attachment; filename=my_todolist_{timestamp}.xls"
    wb = xlwt.Workbook(encoding="utf-8")
    ws = wb.add_sheet("activity")
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ["Задание", "Готовность"]

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


def attach_file_to_task(request: HttpRequest, task_id: int) -> HttpResponse:
    task = ToDo.objects.get(id=task_id)
    if request.method == "POST":
        form = AttachedFileForm(request.POST, request.FILES)
        if form.is_valid():
            attached_file = form.save(commit=False)
            attached_file.task = task
            attached_file.save()
            return redirect("index")
    else:
        form = AttachedFileForm()

    return render(request, "attach_file_to_task.html", {"form": form, "task": task})


def download_file(request: HttpRequest, file_id: int) -> FileResponse:
    attached_file = get_object_or_404(AttachedFile, id=file_id)
    response = FileResponse(attached_file.file, as_attachment=True)
    return response


def delete_attached_file(request: HttpRequest, attached_file_id: int) -> HttpResponse:
    attached_file = get_object_or_404(AttachedFile, id=attached_file_id)
    attached_file.delete()
    return redirect("index")
