# Generated by Django 4.1.5 on 2023-05-02 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0019_alter_genre_name_alter_movie_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='actor',
            old_name='imdb_id',
            new_name='imdb_path',
        ),
    ]
