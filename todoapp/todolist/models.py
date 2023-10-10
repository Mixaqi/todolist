from __future__ import annotations

from django.db import models
import hashlib



class ToDo(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField("Название задания", max_length=500)
    is_complete = models.BooleanField("Завершено", default=False)
    token = models.CharField("Токен", max_length=64, unique=True)


    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs) -> None:
        if not self.token:
            hash_object = hashlib.sha256(self.title.encode())
            self.token = hash_object.hexdigest()
        super().save(*args, **kwargs)
