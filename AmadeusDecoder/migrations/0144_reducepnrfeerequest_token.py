# Generated by Django 3.2.15 on 2022-11-22 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AmadeusDecoder', '0143_merge_20221122_1321'),
    ]

    operations = [
        migrations.AddField(
            model_name='reducepnrfeerequest',
            name='token',
            field=models.CharField(default='iho', max_length=100),
            preserve_default=False,
        ),
    ]
