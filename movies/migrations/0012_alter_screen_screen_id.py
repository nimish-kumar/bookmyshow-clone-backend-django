# Generated by Django 4.1.6 on 2023-04-20 21:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0011_remove_theatre_details"),
    ]

    operations = [
        migrations.AlterField(
            model_name="screen",
            name="screen_id",
            field=models.CharField(max_length=5, unique=True),
        ),
    ]
