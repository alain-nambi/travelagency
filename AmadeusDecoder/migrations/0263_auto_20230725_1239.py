# Generated by Django 3.2.15 on 2023-07-25 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AmadeusDecoder', '0262_merge_20230711_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuration',
            name='created_on',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='configuration',
            name='last_update',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
