# Generated by Django 4.0.6 on 2022-10-17 06:57

import AmadeusDecoder.models.BaseModel
from django.conf import settings
import django.contrib.postgres.fields
import django.contrib.postgres.fields.hstore
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AmadeusDecoder', '0090_ticketpassengersegment_fare_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pnrairsegments',
            name='segment_state',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='PnrHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.IntegerField(default=0)),
                ('number', models.CharField(max_length=100)),
                ('gds_creation_date', models.DateField(null=True)),
                ('system_creation_date', models.DateTimeField(null=True)),
                ('status', models.CharField(default='Non émis', max_length=100)),
                ('status_value', models.IntegerField(default=0)),
                ('exportdate', models.DateTimeField(null=True)),
                ('type', models.CharField(default='Inconnu', max_length=100)),
                ('validationstatus', models.IntegerField(default=0)),
                ('dateexport', models.DateTimeField(null=True)),
                ('changedate', models.DateField(null=True)),
                ('lasttransactiondate', models.DateField(null=True)),
                ('otherinformations', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200, null=True), null=True, size=20)),
                ('ssr', django.contrib.postgres.fields.hstore.HStoreField(null=True)),
                ('openingstatus', models.BooleanField(default=0)),
                ('is_splitted', models.BooleanField(default=0)),
                ('is_duplicated', models.BooleanField(default=0)),
                ('is_parent', models.BooleanField(default=0)),
                ('is_child', models.BooleanField(default=0)),
                ('is_read', models.BooleanField(default=0)),
                ('history_datetime', models.DateTimeField()),
                ('agency', models.ForeignKey(db_column='agency_code', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='history_pnrs', to='AmadeusDecoder.office', to_field='code')),
                ('agent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='history_pnrs', to=settings.AUTH_USER_MODEL)),
                ('currency', models.ForeignKey(db_column='currency_code', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='history_pnrs', to='AmadeusDecoder.currency', to_field='code')),
                ('parent_pnr', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='history_children', to='AmadeusDecoder.pnr')),
                ('pnr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='histories', to='AmadeusDecoder.pnr')),
            ],
            options={
                'db_table': 't_pnr_history',
            },
            bases=(models.Model, AmadeusDecoder.models.BaseModel.BaseModel),
        ),
    ]
