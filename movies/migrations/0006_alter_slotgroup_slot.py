# Generated by Django 4.1.6 on 2023-04-17 21:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0005_rename_descriptiom_movie_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="slotgroup",
            name="slot",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="slotgrp_booking",
                to="movies.bookingslot",
            ),
        ),
    ]
