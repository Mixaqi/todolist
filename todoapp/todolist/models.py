from __future__ import annotations

from django.db import models


class ToDo(models.Model):
    id = models.AutoField(primary_key=True)
    is_complete = models.BooleanField("Завершено", default=False)
    title = models.CharField("Название задания", max_length=500)
    user_id = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"

    def __str__(self) -> str:
        return self.title

class Project(models.Model):
    id = models.AutoField(primary_key=True)
    task_id = models.ForeignKey('ToDo', on_delete=models.CASCADE)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)

class User(models.Model):
    uuid = models.CharField(max_length=255, primary_key=True)
    username = models.CharField(max_length=255)
    email = models.EmailField()
    task_id = models.ForeignKey('ToDo', on_delete=models.SET_NULL, null=True, blank=True)

class AttachedFile(models.Model):
    id = models.AutoField(primary_key=True)
    loader = models.ForeignKey('User', on_delete=models.CASCADE)
    type = models.CharField(max_length=255)
    task_id = models.ForeignKey(ToDo, on_delete=models.CASCADE)  # Используем модель ToDo для связи
    file = models.FileField(upload_to='attached_files/')