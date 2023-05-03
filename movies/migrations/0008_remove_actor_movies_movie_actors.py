# Generated by Django 4.1.5 on 2023-03-01 22:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0007_remove_movie_actors"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="actor",
            name="movies",
        ),
        migrations.AddField(
            model_name="movie",
            name="actors",
            field=models.ManyToManyField(blank=True, to="movies.actor"),
        ),
    ]
