# Generated by Django 4.1.4 on 2023-01-16 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bike_and_terminal', '0002_terminal_latitude_terminal_longitude'),
    ]

    operations = [
        migrations.AlterField(
            model_name='terminal',
            name='latitude',
            field=models.DecimalField(decimal_places=4, max_digits=8),
        ),
        migrations.AlterField(
            model_name='terminal',
            name='longitude',
            field=models.DecimalField(decimal_places=4, max_digits=8),
        ),
    ]