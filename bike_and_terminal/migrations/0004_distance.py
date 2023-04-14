# Generated by Django 4.1.4 on 2023-01-17 07:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bike_and_terminal', '0003_alter_terminal_latitude_alter_terminal_longitude'),
    ]

    operations = [
        migrations.CreateModel(
            name='distance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dist', models.DecimalField(decimal_places=4, default=0.0, max_digits=8)),
                ('term_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bike_and_terminal.terminal')),
            ],
        ),
    ]