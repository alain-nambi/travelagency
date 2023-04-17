# Generated by Django 4.0.6 on 2022-10-06 11:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AmadeusDecoder', '0076_ticket_ticket_type_alter_pnr_system_creation_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='payment_option',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='pnr',
            name='system_creation_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 6, 14, 12, 25, 196149)),
        ),
    ]
