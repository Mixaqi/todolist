# Generated by Django 4.2.5 on 2023-11-06 15:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("todolist", "0013_alter_todo_username"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="assigned_tasks",
        ),
        migrations.AddField(
            model_name="user",
            name="tasks",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="todolist.todo",
            ),
        ),
        migrations.AlterField(
            model_name="todo",
            name="username",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="assigned_tasks",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
