# Generated by Django 4.1.5 on 2023-03-26 20:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0017_alter_genre_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="genre",
            name="name",
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
