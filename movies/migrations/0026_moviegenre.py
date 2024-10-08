# Generated by Django 4.1.5 on 2023-08-01 19:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0025_alter_movie_title"),
    ]

    operations = [
        migrations.CreateModel(
            name="MovieGenre",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "genre_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="movies.genre"
                    ),
                ),
                (
                    "movie_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="movies.movie"
                    ),
                ),
            ],
            options={
                "db_table": "movie_genre",
                "unique_together": {("movie_id", "genre_id")},
            },
        ),
    ]
