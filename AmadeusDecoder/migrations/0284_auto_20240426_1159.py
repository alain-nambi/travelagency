# Generated by Django 3.2.15 on 2024-04-26 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AmadeusDecoder', '0283_auto_20240426_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='unremountedpnrsegment',
            name='order',
            field=models.CharField(max_length=10, null=True),
        ),
    ]