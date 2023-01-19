# Generated by Django 4.1.5 on 2023-01-08 20:35
import os

from django.db import migrations, connection


def load_data_from_sql(apps, schema_editor):
    file_path = os.path.join(os.path.dirname(__file__), '../../data.sql')
    sql_statement = open(file_path).read()
    with connection.cursor() as c:
        c.execute(sql_statement)


class Migration(migrations.Migration):
    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_data_from_sql)
    ]
