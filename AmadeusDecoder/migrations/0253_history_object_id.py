# Generated by Django 4.0 on 2023-06-30 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AmadeusDecoder', '0252_merge_20230627_0958'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='object_id',
            field=models.IntegerField(null=True),
        ),
    ]
