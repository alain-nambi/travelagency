# Generated by Django 3.2.15 on 2022-12-02 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AmadeusDecoder', '0165_merge_20221201_1747'),
    ]

    operations = [
        migrations.AddField(
            model_name='fee',
            name='old_cost',
            field=models.DecimalField(decimal_places=4, default=0.0, max_digits=11),
        )
    ]
