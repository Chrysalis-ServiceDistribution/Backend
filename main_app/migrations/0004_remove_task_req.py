# Generated by Django 5.0.6 on 2024-05-21 19:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='req',
        ),
    ]