# Generated by Django 4.0 on 2023-07-03 07:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AmadeusDecoder', '0256_alter_configuration_single_value'),
    ]

    operations = [
        migrations.RenameField(
            model_name='configuration',
            old_name='last_udpate',
            new_name='last_update',
        ),
    ]
