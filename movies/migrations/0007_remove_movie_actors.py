# Generated by Django 4.1.5 on 2023-03-01 22:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_alter_actor_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='actors',
        ),
    ]
