# Generated by Django 3.2.15 on 2023-01-09 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AmadeusDecoder', '0197_merge_20230107_1027'),
    ]

    operations = [
        # migrations.AddField(
        #     model_name='passengerinvoice',
        #     name='status',
        #     field=models.CharField(max_length=100, null=True),
        # ),
        migrations.AddField(
            model_name='reducepnrfeerequest',
            name='motif',
            field=models.TextField(default='Test', max_length=800),
            preserve_default=False,
        ),
    ]
