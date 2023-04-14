# Generated by Django 4.1.4 on 2023-01-12 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0002_rename_terminal_admins'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='admins',
            name='id',
        ),
        migrations.AddField(
            model_name='admins',
            name='fname',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='admins',
            name='lname',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='admins',
            name='user',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
    ]