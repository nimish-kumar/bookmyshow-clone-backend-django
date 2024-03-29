# Generated by Django 4.1.6 on 2023-03-12 11:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("meta", "0002_city_icon_url_alter_artist_profile_pic_url"),
        ("movies", "0003_alter_movie_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bookingslot",
            name="subtitles_lang",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="subtitle_lang_slots",
                to="meta.language",
            ),
        ),
    ]
