# Generated by Django 4.1.4 on 2023-01-21 17:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bike_and_terminal', '0008_rename_dist_distance'),
    ]

    operations = [
        migrations.CreateModel(
            name='dist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distance', models.DecimalField(decimal_places=4, max_digits=8)),
                ('term_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bike_and_terminal.terminal')),
            ],
        ),
        migrations.DeleteModel(
            name='distance',
        ),
    ]
