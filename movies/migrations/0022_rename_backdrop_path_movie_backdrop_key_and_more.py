# Generated by Django 4.1.5 on 2023-07-02 15:36

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0021_alter_movie_description_alter_movie_duration_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="movie",
            old_name="backdrop_path",
            new_name="backdrop_key",
        ),
        migrations.RenameField(
            model_name="movie",
            old_name="imdb_path",
            new_name="imdb_key",
        ),
        migrations.RenameField(
            model_name="movie",
            old_name="poster_path",
            new_name="poster_key",
        ),
        migrations.RenameField(
            model_name="movie",
            old_name="trailer_path",
            new_name="trailer_key",
        ),
        migrations.RemoveField(
            model_name="movie",
            name="actors",
        ),
        migrations.RemoveField(
            model_name="movie",
            name="genres",
        ),
    ]
