# Generated by Django 4.1.5 on 2023-02-26 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_actor_image_actor_movies'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='description',
            field=models.CharField(max_length=500),
        ),
    ]
