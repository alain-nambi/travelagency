# Generated by Django 4.0 on 2023-06-19 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AmadeusDecoder', '0249_ticket_issuing_agency_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='othersfee',
            name='issuing_agency_name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]