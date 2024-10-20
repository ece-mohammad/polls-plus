# Generated by Django 5.1.1 on 2024-10-08 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("polls", "0004_alter_question_managers_and_more"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="question",
            index=models.Index(
                fields=["pub_date", "exp_date"], name="polls_quest_pub_dat_5ec920_idx"
            ),
        ),
    ]
