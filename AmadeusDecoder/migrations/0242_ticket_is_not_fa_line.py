# Generated by Django 4.1.7 on 2023-03-24 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AmadeusDecoder', '0241_passengerinvoice_status_alter_ticket_flightclass'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='is_not_fa_line',
            field=models.BooleanField(default=0),
        ),
    ]
