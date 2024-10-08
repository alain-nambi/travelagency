# Generated by Django 4.2.6 on 2023-10-09 11:21

import AmadeusDecoder.models.BaseModel
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AmadeusDecoder', '0268_department'),
    ]

    operations = [
        migrations.CreateModel(
            name='Municipality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
                ('code_departement', models.CharField(max_length=255)),
                ('codes_postaux', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 't_municipalities',
            },
            bases=(models.Model, AmadeusDecoder.models.BaseModel.BaseModel),
        ),
    ]
