# Generated by Django 4.0.7 on 2023-01-20 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AmadeusDecoder', '0209_rawdata_ticket'),
    ]

    operations = [
        migrations.AddField(
            model_name='fee',
            name='is_invoiced',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='othersfee',
            name='is_invoiced',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ticket',
            name='is_invoiced',
            field=models.BooleanField(default=False),
        ),
    ]
