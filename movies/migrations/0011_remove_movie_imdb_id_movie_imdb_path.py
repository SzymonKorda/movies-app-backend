# Generated by Django 4.1.5 on 2023-03-19 21:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "movies",
            "0010_genre_remove_actor_born_place_remove_actor_born_year_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="movie",
            name="imdb_id",
        ),
        migrations.AddField(
            model_name="movie",
            name="imdb_path",
            field=models.CharField(default="", max_length=50),
        ),
    ]
