# Generated by Django 4.1.5 on 2023-03-23 18:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0011_remove_movie_imdb_id_movie_imdb_path"),
    ]

    operations = [
        migrations.AlterField(
            model_name="genre",
            name="name",
            field=models.CharField(default="", max_length=50, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name="actor",
            unique_together={("name", "date_of_birth")},
        ),
        migrations.AlterUniqueTogether(
            name="movie",
            unique_together={("title", "release_date")},
        ),
    ]
