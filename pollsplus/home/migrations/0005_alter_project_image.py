# Generated by Django 5.1.1 on 2025-02-18 13:34

import pathlib
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0004_alter_project_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=pathlib.PurePosixPath(
                    "/home/spaghetticheff/Projects/PythonProject/PollsPlus/pollsplus/media/projects"
                ),
            ),
        ),
    ]
