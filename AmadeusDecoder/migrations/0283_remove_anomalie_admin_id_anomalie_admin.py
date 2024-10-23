# Generated by Django 5.0.2 on 2024-02-22 10:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AmadeusDecoder', '0282_alter_anomalie_admin_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='anomalie',
            name='admin_id',
        ),
        migrations.AddField(
            model_name='anomalie',
            name='admin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='admin', to=settings.AUTH_USER_MODEL),
        ),
    ]