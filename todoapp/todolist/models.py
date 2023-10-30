from __future__ import annotations

from django.db import models
from django import forms


class ToDo(models.Model):
    id = models.AutoField(primary_key=True)
    is_complete = models.BooleanField("Завершено", default=False)
    title = models.CharField("Название задания", max_length=500)

    #user = models.ForeignKey("User", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"

    def __str__(self) -> str:
        return self.title


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField("Название проекта", max_length=255, default = "Project")
    task = models.ForeignKey("ToDo", on_delete=models.CASCADE)
    #user = models.ForeignKey("User", on_delete=models.CASCADE)


class User(models.Model):
    uuid = models.CharField(max_length=255, primary_key=True)
    username = models.CharField(max_length=255)
    email = models.EmailField()
    assigned_tasks = models.ForeignKey(
        "ToDo",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_to_user",
    )


class AttachedFile(models.Model):
    id = models.AutoField(primary_key=True)
    # loader = models.ForeignKey('User', on_delete=models.CASCADE)
    # type = models.CharField(max_length=255)
    task = models.ForeignKey(
        ToDo, on_delete=models.CASCADE
    )  # Используем модель ToDo для связи
    file = models.FileField(upload_to="attached_files/", null=True)
