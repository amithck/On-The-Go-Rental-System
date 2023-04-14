# Generated by Django 4.1.4 on 2023-01-10 06:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='terminal',
            fields=[
                ('term_id', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('term_name', models.CharField(max_length=20)),
                ('no_of_bikes', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='bike',
            fields=[
                ('bike_id', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('bike_name', models.CharField(max_length=15)),
                ('bike_type', models.CharField(choices=[('ev', 'electric'), ('fe', 'fuel')], max_length=2)),
                ('rent_cost', models.IntegerField()),
                ('term_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bike_and_terminal.terminal')),
            ],
        ),
    ]
