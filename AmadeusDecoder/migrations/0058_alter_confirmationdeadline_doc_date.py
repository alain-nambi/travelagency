# Generated by Django 4.0.6 on 2022-09-23 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AmadeusDecoder', '0057_alter_remark_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='confirmationdeadline',
            name='doc_date',
            field=models.DateTimeField(),
        ),
    ]
