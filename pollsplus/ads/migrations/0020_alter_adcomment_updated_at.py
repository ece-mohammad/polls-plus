# Generated by Django 5.1.1 on 2025-02-20 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ads", "0019_adcomment_updated_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="adcomment",
            name="updated_at",
            field=models.DateTimeField(
                blank=True,
                help_text="Last time the comment was updated",
                null=True,
                verbose_name="Updated at",
            ),
        ),
    ]
