# Generated by Django 4.1.5 on 2023-02-20 20:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0003_alter_movie_actors"),
    ]

    operations = [
        migrations.AlterField(
            model_name="movie",
            name="description",
            field=models.CharField(max_length=500),
        ),
    ]
