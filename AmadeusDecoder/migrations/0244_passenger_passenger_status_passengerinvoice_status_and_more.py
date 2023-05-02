# Generated by Django 4.1.7 on 2023-04-19 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AmadeusDecoder', '0243_merge_20230328_1539'),
    ]

    operations = [
        migrations.AddField(
            model_name='passenger',
            name='passenger_status',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='passengerinvoice',
            name='status',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='is_ticket_modification',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='ticket',
            name='original_ticket_status',
            field=models.IntegerField(default=1),
        ),
    ]