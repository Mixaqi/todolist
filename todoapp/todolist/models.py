from __future__ import annotations

from django.db import models


class ToDo(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField("Название задания", max_length=500)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    attached_files = models.ManyToManyField('AttachedFile')

    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"

    def __str__(self) -> str:
        return self.title

class Project(models.Model):
    id = models.AutoField(primary_key=True)
    task_id = models.ForeignKey('Task', on_delete=models.CASCADE)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)

class User(models.Model):
    uuid = models.CharField(max_length=255, primary_key=True)
    username = models.CharField(max_length=255)
    email = models.EmailField()
    task_id = models.IntegerField()

class AttachedFile(models.Model):
    id = models.AutoField(primary_key=True)
    loader = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    task_id = models.ForeignKey('Task', on_delete=models.CASCADE)