# Generated by Django 4.0.6 on 2022-10-19 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AmadeusDecoder', '0097_merge_20221019_1710'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='is_pnr',
            field=models.BooleanField(default=True),
        ),
    ]
