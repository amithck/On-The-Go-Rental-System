# Generated by Django 4.1.4 on 2023-01-21 17:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bike_and_terminal', '0012_distance_delete_dist'),
    ]

    operations = [
        migrations.DeleteModel(
            name='distance',
        ),
    ]