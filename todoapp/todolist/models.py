from __future__ import annotations

from django.contrib.auth.models import User
from django.db import models


class ToDo(models.Model):
    id = models.AutoField(primary_key=True)
    is_complete = models.BooleanField("Завершено", default=False)
    title = models.CharField("Название задания", max_length=500)
    username = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"

    def __str__(self) -> str:
        return self.title


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField("Название проекта", max_length=255, default="Project")
    task = models.ForeignKey("ToDo", on_delete=models.CASCADE)
    # user = models.ForeignKey("User", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title


class AttachedFile(models.Model):
    id = models.AutoField(primary_key=True)
    task = models.ForeignKey(
        ToDo,
        on_delete=models.CASCADE,
    )
    file = models.FileField(upload_to="attached_files/", null=True)

    def __str__(self) -> str:
        return self.file.name
