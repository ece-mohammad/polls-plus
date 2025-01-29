# Generated by Django 5.1.1 on 2025-01-29 08:09

import ads.models
import django.db.models.deletion
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ads", "0007_rename_advertisement_ad_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="ad",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True,
                help_text="When the advertisement was created",
                verbose_name="Created at",
            ),
        ),
        migrations.AlterField(
            model_name="ad",
            name="owner",
            field=models.ForeignKey(
                help_text="User that created the advertisement",
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created by",
            ),
        ),
        migrations.AlterField(
            model_name="ad",
            name="price",
            field=models.DecimalField(
                decimal_places=2,
                default=Decimal("0"),
                help_text="Price for your advertisement",
                max_digits=7,
                verbose_name="Price",
            ),
        ),
        migrations.AlterField(
            model_name="ad",
            name="text",
            field=models.TextField(
                default="",
                help_text="Description for your advertisement",
                null=True,
                verbose_name="Description",
            ),
        ),
        migrations.AlterField(
            model_name="ad",
            name="title",
            field=models.CharField(
                help_text="Title for your advertisement",
                max_length=200,
                validators=[ads.models.AdTitleValidator(2)],
                verbose_name="Title",
            ),
        ),
        migrations.AlterField(
            model_name="ad",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True,
                help_text="Last time the advertisement was updated",
                verbose_name="Updated at",
            ),
        ),
        migrations.AlterField(
            model_name="historicalad",
            name="created_at",
            field=models.DateTimeField(
                blank=True,
                editable=False,
                help_text="When the advertisement was created",
                verbose_name="Created at",
            ),
        ),
        migrations.AlterField(
            model_name="historicalad",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                help_text="User that created the advertisement",
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created by",
            ),
        ),
        migrations.AlterField(
            model_name="historicalad",
            name="price",
            field=models.DecimalField(
                decimal_places=2,
                default=Decimal("0"),
                help_text="Price for your advertisement",
                max_digits=7,
                verbose_name="Price",
            ),
        ),
        migrations.AlterField(
            model_name="historicalad",
            name="text",
            field=models.TextField(
                default="",
                help_text="Description for your advertisement",
                null=True,
                verbose_name="Description",
            ),
        ),
        migrations.AlterField(
            model_name="historicalad",
            name="title",
            field=models.CharField(
                help_text="Title for your advertisement",
                max_length=200,
                validators=[ads.models.AdTitleValidator(2)],
                verbose_name="Title",
            ),
        ),
        migrations.AlterField(
            model_name="historicalad",
            name="updated_at",
            field=models.DateTimeField(
                blank=True,
                editable=False,
                help_text="Last time the advertisement was updated",
                verbose_name="Updated at",
            ),
        ),
    ]
