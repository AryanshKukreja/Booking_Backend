# Generated by Django 5.0.6 on 2025-05-15 06:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_create_time_slots'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timeslot',
            name='minute',
        ),
    ]
