# Generated by Django 4.0.7 on 2022-09-29 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AmadeusDecoder', '0063_ticket_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gds_id',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
