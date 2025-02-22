# Generated by Django 5.1.6 on 2025-02-22 01:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ads", "0024_remove_adcomment_image_ad_image_historicalad_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ad",
            name="image",
            field=models.ImageField(
                blank=True,
                help_text="Image for your advertisement",
                null=True,
                upload_to="ads",
                validators=[
                    django.core.validators.MaxLengthValidator(
                        2097152, "Image must be less than 2.00 MB"
                    )
                ],
                verbose_name="Image",
            ),
        ),
        migrations.AlterField(
            model_name="historicalad",
            name="image",
            field=models.TextField(
                blank=True,
                help_text="Image for your advertisement",
                max_length=100,
                null=True,
                validators=[
                    django.core.validators.MaxLengthValidator(
                        2097152, "Image must be less than 2.00 MB"
                    )
                ],
                verbose_name="Image",
            ),
        ),
    ]
