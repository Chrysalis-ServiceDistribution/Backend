# Generated by Django 5.0.6 on 2024-05-21 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_remove_task_req'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('P', 'Pending'), ('A', 'Accepted'), ('IP', 'In Progress'), ('C', 'Completed'), ('X', 'Cancelled')], default='P', max_length=2),
        ),
    ]
