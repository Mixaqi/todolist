# Generated by Django 4.2.5 on 2023-11-05 19:08

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("todolist", "0010_remove_todo_user_project_title"),
    ]

    operations = [
        migrations.DeleteModel(
            name="User",
        ),
    ]