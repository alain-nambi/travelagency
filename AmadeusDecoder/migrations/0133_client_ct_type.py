# Generated by Django 4.0.7 on 2022-11-14 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AmadeusDecoder', '0132_client_classment_client_code_postal_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='ct_type',
            field=models.IntegerField(default=False),
        ),
    ]
