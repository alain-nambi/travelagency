# Generated by Django 4.0.6 on 2022-10-03 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AmadeusDecoder', '0069_merge_20220930_1511'),
    ]

    operations = [
        migrations.AddField(
            model_name='pnr',
            name='is_read',
            field=models.BooleanField(default=0),
        ),
    ]
