# Generated by Django 4.1.6 on 2023-02-12 04:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={},
        ),
        migrations.AddIndex(
            model_name="user",
            index=models.Index(fields=["email"], name="usr_email_idx"),
        ),
        migrations.AddIndex(
            model_name="user",
            index=models.Index(
                fields=["first_name", "last_name"], name="usr_names_idx"
            ),
        ),
    ]
