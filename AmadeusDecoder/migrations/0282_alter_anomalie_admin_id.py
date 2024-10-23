# Generated by Django 5.0.2 on 2024-02-22 09:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AmadeusDecoder', '0281_merge_20240222_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anomalie',
            name='admin_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='admin_id', to=settings.AUTH_USER_MODEL),
        ),
    ]