# Generated by Django 4.0.6 on 2022-10-11 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AmadeusDecoder', '0087_alter_pnr_system_creation_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pnrairsegments',
            name='timecheckin',
            field=models.TimeField(null=True),
        ),
    ]
