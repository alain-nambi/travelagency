# Generated by Django 3.2.15 on 2024-01-09 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AmadeusDecoder', '0269_municipality'),
    ]

    operations = [
        migrations.AlterField(
            model_name='othersfee',
            name='creation_date',
            field=models.DateTimeField(null=True),
        ),
    ]
