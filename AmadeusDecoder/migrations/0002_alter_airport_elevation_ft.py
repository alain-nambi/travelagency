# Generated by Django 4.0.6 on 2022-08-29 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AmadeusDecoder', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='airport',
            name='elevation_ft',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
