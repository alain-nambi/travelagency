# Generated by Django 3.2.15 on 2023-02-04 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AmadeusDecoder', '0223_merge_20230204_1111'),
    ]

    operations = [
        # migrations.AddField(
        #     model_name='passengerinvoice',
        #     name='invoice_number',
        #     field=models.CharField(default=None, max_length=100, null=True),
        # ),
        # migrations.AddField(
        #     model_name='passengerinvoice',
        #     name='status',
        #     field=models.CharField(max_length=100, null=True),
        # ),
        migrations.AlterField(
            model_name='othersfee',
            name='creation_date',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]
