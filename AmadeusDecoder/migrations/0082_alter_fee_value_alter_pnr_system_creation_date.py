# Generated by Django 4.0.6 on 2022-10-07 08:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AmadeusDecoder', '0081_alter_fee_pnr_alter_fee_ticket_alter_fee_value_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fee',
            name='value',
            field=models.DecimalField(decimal_places=4, max_digits=11, null=True),
        ),
        migrations.AlterField(
            model_name='pnr',
            name='system_creation_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 7, 11, 47, 31, 403009)),
        ),
    ]
