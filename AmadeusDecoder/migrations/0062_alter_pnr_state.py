# Generated by Django 4.0.6 on 2022-09-28 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AmadeusDecoder', '0061_merge_20220927_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pnr',
            name='state',
            field=models.IntegerField(default=0),
        ),
    ]
