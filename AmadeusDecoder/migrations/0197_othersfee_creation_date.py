# Generated by Django 4.0.6 on 2023-01-10 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AmadeusDecoder', '0196_passengerinvoice_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='othersfee',
            name='creation_date',
            field=models.DateField(null=True),
        ),
    ]
