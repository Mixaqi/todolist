from __future__ import annotations

import csv
import datetime
from typing import TYPE_CHECKING

import xlwt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import AttachedFileForm
from .models import AttachedFile, ToDo

if TYPE_CHECKING:
    from django.http import FileResponse, HttpRequest, HttpResponse


@login_required
def index(request: HttpRequest) -> HttpResponse:
    user = request.user  # Получить текущего пользователя
    todos = ToDo.objects.filter(username=user)  # Фильтровать задачи только для текущего пользователя
    return render(
        request,
        "todoapp/index.html",
        {"todo_list": todos, "title": "Главная страница"},
    )


@login_required
@require_http_methods(["POST"])
def add(request: HttpRequest) -> HttpResponse:
    title = request.POST["title"]
    if len(title) != 0:
        user = request.user  # Получить текущего пользователя
        todo = ToDo(title=title, username=user)
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


def user_login(request: HttpRequest) -> HttpResponse:
    if request.POST:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user=user)
            return redirect("index")
    return render(request, "todoapp/login.html")


def user_logout(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("login")


# @login_required
# def tasks_with_files(request: HttpRequest) -> HttpResponse:
#     tasks = ToDo.objects.filter(user=request.user).select_related("attachedfile_set")
#     return render(request, "index.html", {"tasks": tasks})


# def save(self, *args, **kwargs) -> None:
#     if not self.user:
#         current_user = self._meta.model.user
#         if current_user:
#             self.user = current_user
 #     super().save(*args, **kwargs)