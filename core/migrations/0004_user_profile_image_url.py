# Generated by Django 4.1.6 on 2023-05-01 14:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_user_reviewer_type_review_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="profile_image_url",
            field=models.URLField(blank=True, null=True),
        ),
    ]