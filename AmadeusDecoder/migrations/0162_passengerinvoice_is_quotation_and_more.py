# Generated by Django 4.0.7 on 2022-12-01 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AmadeusDecoder', '0161_client_departement_passengerinvoice_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='passengerinvoice',
            name='is_quotation',
            field=models.BooleanField(default=False),
        ),
    ]
