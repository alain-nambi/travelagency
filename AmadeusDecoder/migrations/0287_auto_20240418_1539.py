# Generated by Django 3.2.15 on 2024-04-18 12:39

import AmadeusDecoder.models.BaseModel
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AmadeusDecoder', '0286_auto_20240418_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anomalie',
            name='categorie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AmadeusDecoder.categorieanomalie'),
        )
    ]