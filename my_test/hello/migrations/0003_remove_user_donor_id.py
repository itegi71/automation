# Generated by Django 5.1.3 on 2025-03-06 18:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0002_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='donor_id',
        ),
    ]
