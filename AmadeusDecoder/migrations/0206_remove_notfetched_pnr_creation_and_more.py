# Generated by Django 4.0.7 on 2023-01-12 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AmadeusDecoder', '0205_passengerinvoice_status_notfetched'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notfetched',
            name='pnr_creation',
        ),
    ]
