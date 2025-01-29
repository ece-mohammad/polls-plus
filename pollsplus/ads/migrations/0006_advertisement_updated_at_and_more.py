# Generated by Django 5.1.1 on 2025-01-09 04:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ads", "0005_remove_advertisement_updated_at_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="advertisement",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="historicaladvertisement",
            name="updated_at",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime(
                    2025, 1, 9, 4, 15, 58, 691006, tzinfo=datetime.timezone.utc
                ),
                editable=False,
            ),
            preserve_default=False,
        ),
    ]
