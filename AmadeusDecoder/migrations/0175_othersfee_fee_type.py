# Generated by Django 4.0.6 on 2022-12-14 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AmadeusDecoder', '0174_ticket_is_no_adc'),
    ]

    operations = [
        migrations.AddField(
            model_name='othersfee',
            name='fee_type',
            field=models.CharField(default='Other_fee', max_length=100),
        ),
    ]
