# Generated by Django 4.1.5 on 2023-07-08 14:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0022_rename_backdrop_path_movie_backdrop_key_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="movie",
            name="id",
        ),
        migrations.AddField(
            model_name="movie",
            name="movie_id",
            field=models.BigAutoField(primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
