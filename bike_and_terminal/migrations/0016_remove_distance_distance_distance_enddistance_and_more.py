# Generated by Django 4.1.4 on 2023-01-22 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bike_and_terminal', '0015_alter_distance_distance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='distance',
            name='distance',
        ),
        migrations.AddField(
            model_name='distance',
            name='enddistance',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='distance',
            name='startdistance',
            field=models.CharField(default='', max_length=20),
        ),
    ]