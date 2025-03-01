# Generated by Django 5.1.1 on 2025-02-19 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [
        ("home", "0001_initial"),
        ("home", "0002_alter_project_image"),
        ("home", "0003_alter_project_image"),
        ("home", "0004_alter_project_image"),
        ("home", "0005_alter_project_image"),
        ("home", "0006_alter_project_image"),
        ("home", "0007_alter_project_options"),
        ("home", "0008_alter_project_options_alter_project_status"),
        ("home", "0009_alter_project_status"),
        ("home", "0010_alter_project_status"),
        ("home", "0011_alter_project_options_alter_project_status"),
    ]

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("description", models.TextField()),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="projects/"),
                ),
                ("url", models.CharField(max_length=200)),
                ("github_url", models.URLField(blank=True)),
                ("demo_url", models.URLField(blank=True)),
                ("docs_url", models.URLField(blank=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Live", "Live"),
                            ("Beta", "Beta"),
                            ("Development", "Development"),
                        ],
                        max_length=20,
                    ),
                ),
                ("version", models.CharField(max_length=10)),
                (
                    "rating",
                    models.DecimalField(
                        blank=True, decimal_places=1, max_digits=2, null=True
                    ),
                ),
                ("categories", models.JSONField(default=list)),
                ("technologies", models.JSONField(default=list)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["status", "-updated_at", "-created_at"],
            },
        ),
    ]
