# Generated by Django 3.2.15 on 2024-03-20 14:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AmadeusDecoder', '0281_alter_reducepnrfeerequest_system_creation_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='anomalie',
            name='admin_id',
        ),
    ]
