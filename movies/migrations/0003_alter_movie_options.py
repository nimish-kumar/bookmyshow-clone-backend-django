# Generated by Django 4.1.6 on 2023-03-12 04:08

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0002_alter_bookingslot_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="movie",
            options={"ordering": ["-id"]},
        ),
    ]