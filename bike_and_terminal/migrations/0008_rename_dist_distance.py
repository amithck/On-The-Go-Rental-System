# Generated by Django 4.1.4 on 2023-01-21 17:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bike_and_terminal', '0007_dist_delete_distance'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='dist',
            new_name='distance',
        ),
    ]
