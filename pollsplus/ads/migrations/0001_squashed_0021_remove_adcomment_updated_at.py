# Generated by Django 5.1.1 on 2025-02-20 18:38

import ads.models
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import simple_history.models
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [
        ("ads", "0001_initial"),
        ("ads", "0002_historicaladvertisement"),
        ("ads", "0003_alter_advertisement_text_and_more"),
        ("ads", "0004_alter_advertisement_text_and_more"),
        ("ads", "0005_remove_advertisement_updated_at_and_more"),
        ("ads", "0006_advertisement_updated_at_and_more"),
        ("ads", "0007_rename_advertisement_ad_and_more"),
        ("ads", "0008_alter_ad_created_at_alter_ad_owner_alter_ad_price_and_more"),
        ("ads", "0009_adcomment_ad_comments"),
        ("ads", "0010_remove_ad_comments"),
        ("ads", "0011_alter_adcomment_ad_alter_adcomment_author"),
        ("ads", "0012_alter_adcomment_author"),
        ("ads", "0013_alter_adcomment_author"),
        ("ads", "0014_alter_adcomment_author_adimage"),
        ("ads", "0015_adimage_uploaded_at"),
        ("ads", "0016_rename_owner_ad_author_and_more"),
        ("ads", "0017_alter_adcomment_options"),
        ("ads", "0018_alter_adcomment_text"),
        ("ads", "0019_adcomment_updated_at"),
        ("ads", "0020_alter_adcomment_updated_at"),
        ("ads", "0021_remove_adcomment_updated_at"),
    ]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Ad",
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
                (
                    "title",
                    models.CharField(
                        help_text="Title for your advertisement",
                        max_length=200,
                        validators=[ads.models.AdTitleValidator(2)],
                        verbose_name="Title",
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        default=Decimal("0"),
                        help_text="Price for your advertisement",
                        max_digits=7,
                        verbose_name="Price",
                    ),
                ),
                (
                    "text",
                    models.TextField(
                        default="",
                        help_text="Description for your advertisement",
                        null=True,
                        verbose_name="Description",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="When the advertisement was created",
                        verbose_name="Created at",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        help_text="User that created the advertisement",
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created by",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True,
                        help_text="Last time the advertisement was updated",
                        verbose_name="Updated at",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="HistoricalAd",
            fields=[
                (
                    "id",
                    models.BigIntegerField(
                        auto_created=True, blank=True, db_index=True, verbose_name="ID"
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        help_text="Title for your advertisement",
                        max_length=200,
                        validators=[ads.models.AdTitleValidator(2)],
                        verbose_name="Title",
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        default=Decimal("0"),
                        help_text="Price for your advertisement",
                        max_digits=7,
                        verbose_name="Price",
                    ),
                ),
                (
                    "text",
                    models.TextField(
                        default="",
                        help_text="Description for your advertisement",
                        null=True,
                        verbose_name="Description",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        blank=True,
                        editable=False,
                        help_text="When the advertisement was created",
                        verbose_name="Created at",
                    ),
                ),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField(db_index=True)),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
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
                (
                    "updated_at",
                    models.DateTimeField(
                        blank=True,
                        editable=False,
                        help_text="Last time the advertisement was updated",
                        verbose_name="Updated at",
                    ),
                ),
            ],
            options={
                "verbose_name": "historical ad",
                "verbose_name_plural": "historical ads",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="AdImage",
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
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        help_text="Image for your advertisement",
                        null=True,
                        upload_to="ads",
                        validators=[
                            django.core.validators.MaxLengthValidator(
                                2097152, "Image must be less than 2 MB"
                            )
                        ],
                        verbose_name="Image",
                    ),
                ),
                (
                    "ad",
                    models.ForeignKey(
                        help_text="Ad that this image belongs to",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        related_query_name="image",
                        to="ads.ad",
                        verbose_name="Ad",
                    ),
                ),
                (
                    "uploaded_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        default=django.utils.timezone.now,
                        help_text="When the image was uploaded",
                        verbose_name="Created at",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="AdComment",
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
                (
                    "text",
                    models.TextField(
                        help_text="Comment for your advertisement",
                        validators=[
                            django.core.validators.MinLengthValidator(
                                2, "Comment must be at least 2 characters long"
                            )
                        ],
                        verbose_name="Comment",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="When the comment was created",
                        verbose_name="Created at",
                    ),
                ),
                (
                    "ad",
                    models.ForeignKey(
                        help_text="Ad that this comment belongs to",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        related_query_name="comment",
                        to="ads.ad",
                        verbose_name="Ad",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        help_text="User that created the comment",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created by",
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
