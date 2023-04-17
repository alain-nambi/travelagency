# Generated by Django 4.0.6 on 2022-08-29 08:10

import AmadeusDecoder.models.BaseModel
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
                ('state', models.IntegerField()),
                ('duration', models.IntegerField()),
            ],
            options={
                'db_table': 't_activation',
            },
            bases=(models.Model, AmadeusDecoder.models.BaseModel.BaseModel),
        ),
        migrations.CreateModel(
            name='Airline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('alias', models.CharField(max_length=200, null=True)),
                ('iata', models.CharField(max_length=200, null=True)),
                ('icao', models.CharField(max_length=200, null=True)),
                ('callsign', models.CharField(max_length=200, null=True)),
                ('country', models.CharField(max_length=200, null=True)),
                ('active', models.CharField(max_length=200, null=True)),
            ],
            options={
                'db_table': 't_airlines',
            },
            bases=(models.Model, AmadeusDecoder.models.BaseModel.BaseModel),
        ),
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ident', models.CharField(max_length=200, null=True)),
                ('type', models.CharField(max_length=200, null=True)),
                ('name', models.CharField(max_length=200)),
                ('elevation_ft', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('continent', models.CharField(max_length=200, null=True)),
                ('iso_country', models.CharField(max_length=200, null=True)),
                ('iso_region', models.CharField(max_length=200, null=True)),
                ('municipality', models.CharField(max_length=200, null=True)),
                ('gps_code', models.CharField(max_length=200, null=True)),
                ('iata_code', models.CharField(max_length=200, null=True)),
                ('local_code', models.CharField(max_length=200, null=True)),
                ('coordinates', models.CharField(max_length=200, null=True)),
            ],
            options={
                'db_table': 't_airports',
            },
            bases=(models.Model, AmadeusDecoder.models.BaseModel.BaseModel),
        ),
        migrations.CreateModel(
            name='ClassSign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50)),
                ('gdsprovider', models.CharField(max_length=100)),
                ('sign', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=10, null=True), size=8)),
            ],
            options={
                'db_table': 't_classsign',
            },
            bases=(models.Model, AmadeusDecoder.models.BaseModel.BaseModel),
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=200)),
                ('first_name', models.CharField(max_length=200)),
                ('address_1', models.CharField(max_length=200)),
                ('address_2', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=100)),
                ('customer_type', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('order_type', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 't_client',
            },
            bases=(models.Model, AmadeusDecoder.models.BaseModel.BaseModel),
        ),
        migrations.CreateModel(
            name='ClientAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 't_client_address',
            },
            bases=(models.Model, AmadeusDecoder.models.BaseModel.BaseModel),
        ),
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
                ('attribute', models.IntegerField()),
                ('value', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 't_config',
            },
            bases=(models.Model, AmadeusDecoder.models.BaseModel.BaseModel),
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contacttype', models.CharField(max_length=100, null=True)),
                ('value', models.CharField(max_length=200, null=True)),
                ('owner', models.CharField(max_length=200, null=True)),
            ],
            options={
                'db_table': 't_pnr_contact',
            },
            bases=(models.Model, AmadeusDecoder.models.BaseModel.BaseModel),
        ),
        migrations.CreateModel(
            name='Continent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('code', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 't_continents',
            },
            bases=(models.Model, AmadeusDecoder.models.BaseModel.BaseModel),
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('code', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 't_countries',
            },
            bases=(models.Model, AmadeusDecoder.models.BaseModel.BaseModel),
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('code', models.CharField(max_length=5)),
            ],
            options={
                'db_table': 't_currency',
            },
            bases=(models.Model, AmadeusDecoder.models.BaseModel.BaseModel),
        ),
        migrations.CreateModel(
            name='FlightClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flightclass', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 't_flightclass',
            },
            bases=(models.Model, AmadeusDecoder.models.BaseModel.BaseModel),
        ),
        migrations.CreateModel(
            name='FlightType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 't_flighttype',
            },
            bases=(models.Model, AmadeusDecoder.models.BaseModel.BaseModel),
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transmitter', models.CharField(max_length=200, null=True)),
                ('follow', models.CharField(max_length=200, null=True)),
                ('reference', models.CharField(max_length=200, null=True)),
                ('type', models.CharField(max_length=200, null=True)),
                ('transmission_date', models.DateField(null=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AmadeusDecoder.client')),
            ],
            options={
                'db_table': 't_invoice',
            },
            bases=(models.Model, AmadeusDecoder.models.BaseModel.BaseModel),
        ),
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('surname', models.CharField(max_length=200, null=True)),
                ('designation', models.CharField(max_length=20, null=True)),
                ('birthdate', models.DateField(null=True)),
            ],
            options={
                'db_table': 't_passengers',
            },
            bases=(models.Model, AmadeusDecoder.models.BaseModel.BaseModel),
        ),
        migrations.CreateModel(
            name='Pnr',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=100)),
                ('creationdate', models.DateField(null=True)),
                ('exportstatus', models.IntegerField(default=0)),
                ('exportdate', models.DateTimeField(null=True)),
                ('type', models.CharField(default='Inconnu', max_length=100)),
                ('validationstatus', models.IntegerField(default=0)),
                ('dateexport', models.DateTimeField(null=True)),
                ('changedate', models.DateField(null=True)),
                ('lasttransactiondate', models.DateField(null=True)),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='currency_code', to='AmadeusDecoder.currency', to_field='code')),
            ],
            options={
                'db_table': 't_pnr',
            },
            bases=(models.Model, AmadeusDecoder.models.BaseModel.BaseModel),
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=200)),
                ('path', models.CharField(max_length=200, null=True)),
                ('transport_cost', models.DecimalField(decimal_places=4, default=0, max_digits=11)),
                ('tax', models.DecimalField(decimal_places=4, default=0, max_digits=11)),
                ('total', models.DecimalField(decimal_places=4, default=0, max_digits=11)),
                ('passengerpath', models.CharField(max_length=200, null=True)),
                ('flightclass', models.CharField(max_length=200)),
                ('referenceticket', models.CharField(max_length=200, null=True)),
                ('status', models.CharField(max_length=200, null=True)),
                ('doccurrency', models.CharField(max_length=200, null=True)),
                ('farecurrency', models.CharField(max_length=200, null=True)),
                ('fare', models.DecimalField(decimal_places=4, default=0, max_digits=11)),
                ('fareequiv', models.DecimalField(decimal_places=4, default=0, max_digits=11)),
                ('farerate', models.DecimalField(decimal_places=4, default=0, max_digits=11)),
                ('commission', models.CharField(max_length=200, null=True)),
                ('origcity', models.CharField(max_length=200, null=True)),
                ('destcity', models.CharField(max_length=200, null=True)),
                ('paxtype', models.CharField(max_length=200, null=True)),
                ('passenger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AmadeusDecoder.passenger')),
                ('pnr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AmadeusDecoder.pnr')),
            ],
            options={
                'db_table': 't_ticket',
            },
            bases=(models.Model, AmadeusDecoder.models.BaseModel.BaseModel),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('surname', models.CharField(max_length=200)),
                ('username', models.CharField(max_length=200)),
                ('email_password', models.CharField(max_length=300)),
                ('birth_date', models.DateField()),
                ('type', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 't_user',
            },
            bases=(models.Model, AmadeusDecoder.models.BaseModel.BaseModel),
        ),
        migrations.CreateModel(
            name='ticketHistories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=200, null=True)),
                ('actiondate', models.DateTimeField(null=True)),
                ('agentsign', models.CharField(max_length=200, null=True)),
                ('nationalamount', models.DecimalField(decimal_places=4, default=0, max_digits=11)),
                ('nationalcurrency', models.CharField(max_length=200, null=True)),
                ('markuptotal', models.DecimalField(decimal_places=4, default=0, max_digits=11)),
                ('markupvat', models.DecimalField(decimal_places=4, default=0, max_digits=11)),
                ('markupdiscount', models.DecimalField(decimal_places=4, default=0, max_digits=11)),
                ('creditcurrencyrate', models.DecimalField(decimal_places=4, default=0, max_digits=11)),
                ('documentcredittotal', models.DecimalField(decimal_places=4, default=0, max_digits=11)),
                ('amount', models.DecimalField(decimal_places=4, default=0, max_digits=11)),
                ('servicefeediscount', models.DecimalField(decimal_places=4, default=0, max_digits=11)),
                ('sftotal', models.DecimalField(decimal_places=4, default=0, max_digits=11)),
                ('sftotalvat', models.DecimalField(decimal_places=4, default=0, max_digits=11)),
                ('sfsubagent', models.DecimalField(decimal_places=4, default=0, max_digits=11)),
                ('sfsubagentret', models.DecimalField(decimal_places=4, default=0, max_digits=11)),
                ('sfsubagentvat', models.DecimalField(decimal_places=4, default=0, max_digits=11)),
                ('sfsubagentvatret', models.DecimalField(decimal_places=4, default=0, max_digits=11)),
                ('sfconsolidator', models.DecimalField(decimal_places=4, default=0, max_digits=11)),
                ('sfconsolidatorvat', models.DecimalField(decimal_places=4, default=0, max_digits=11)),
                ('sfconsolidatorret', models.DecimalField(decimal_places=4, default=0, max_digits=11)),
                ('currency', models.CharField(max_length=200, null=True)),
                ('farepaid', models.DecimalField(decimal_places=4, default=0, max_digits=11)),
                ('fareused', models.DecimalField(decimal_places=4, default=0, max_digits=11)),
                ('farerefund', models.DecimalField(decimal_places=4, default=0, max_digits=11)),
                ('netrefund', models.DecimalField(decimal_places=4, default=0, max_digits=11)),
                ('cancellationfee', models.DecimalField(decimal_places=4, default=0, max_digits=11)),
                ('miscallaneousfee', models.DecimalField(decimal_places=4, default=0, max_digits=11)),
                ('taxrefund', models.DecimalField(decimal_places=4, default=0, max_digits=11)),
                ('refundtotal', models.DecimalField(decimal_places=4, default=0, max_digits=11)),
                ('docissuedate', models.DateField(null=True)),
                ('departuredate', models.DateField(null=True)),
                ('comission', models.CharField(max_length=200, null=True)),
                ('sfconsolidatorvatret', models.CharField(max_length=200, null=True)),
                ('creditcurrency', models.CharField(max_length=200, null=True)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AmadeusDecoder.ticket')),
            ],
            options={
                'db_table': 't_histories',
            },
            bases=(models.Model, AmadeusDecoder.models.BaseModel.BaseModel),
        ),
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=4, default=0, max_digits=11)),
                ('taxcode', models.CharField(max_length=200, null=True)),
                ('naturecode', models.CharField(max_length=200, null=True)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tax_related_ticket', to='AmadeusDecoder.ticket')),
            ],
            options={
                'db_table': 't_taxes',
            },
            bases=(models.Model, AmadeusDecoder.models.BaseModel.BaseModel),
        ),
        migrations.CreateModel(
            name='ServiceFees',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=4, default=0, max_digits=11)),
                ('flightclassid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AmadeusDecoder.flightclass')),
                ('flighttype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AmadeusDecoder.flighttype')),
            ],
            options={
                'db_table': 't_servicefees',
            },
            bases=(models.Model, AmadeusDecoder.models.BaseModel.BaseModel),
        ),
        migrations.CreateModel(
            name='PnrPassenger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passenger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AmadeusDecoder.passenger')),
                ('pnr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AmadeusDecoder.pnr')),
            ],
            options={
                'db_table': 't_pnr_passengers',
            },
            bases=(models.Model, AmadeusDecoder.models.BaseModel.BaseModel),
        ),
        migrations.CreateModel(
            name='PnrAirSegments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flightno', models.CharField(max_length=50, null=True)),
                ('bkgclass', models.CharField(max_length=50, null=True)),
                ('departuretime', models.DateTimeField(null=True)),
                ('arrivaltime', models.DateTimeField(null=True)),
                ('amanameorg', models.CharField(max_length=200, null=True)),
                ('countryorg', models.CharField(max_length=200, null=True)),
                ('amanamedest', models.CharField(max_length=200, null=True)),
                ('countrydest', models.CharField(max_length=200, null=True)),
                ('baggageallow', models.CharField(max_length=200, null=True)),
                ('terminalcheckin', models.CharField(max_length=200, null=True)),
                ('timecheckin', models.DateTimeField(null=True)),
                ('codedest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination_airport', to='AmadeusDecoder.airport', to_field='iata_code')),
                ('codeorg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='origin_airport', to='AmadeusDecoder.airport', to_field='iata_code')),
                ('pnr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AmadeusDecoder.pnr')),
                ('servicecarrier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AmadeusDecoder.airline')),
            ],
            options={
                'db_table': 't_pnrairsegments',
            },
            bases=(models.Model, AmadeusDecoder.models.BaseModel.BaseModel),
        ),
        migrations.CreateModel(
            name='PassengerAttribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=200, null=True)),
                ('passenger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AmadeusDecoder.passenger')),
            ],
            options={
                'db_table': 't_passenger_additional_infos',
            },
            bases=(models.Model, AmadeusDecoder.models.BaseModel.BaseModel),
        ),
        migrations.CreateModel(
            name='InvoiceDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('totalht', models.DecimalField(decimal_places=4, default=0, max_digits=11)),
                ('tva_sce', models.DecimalField(decimal_places=4, default=0, max_digits=11)),
                ('total', models.DecimalField(decimal_places=4, default=0, max_digits=11)),
                ('duedate', models.DateField(null=True)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AmadeusDecoder.invoice')),
            ],
            options={
                'db_table': 't_invoice_detail',
            },
            bases=(models.Model, AmadeusDecoder.models.BaseModel.BaseModel),
        ),
        migrations.AddField(
            model_name='invoice',
            name='pnr',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AmadeusDecoder.pnr'),
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('airlinecode', models.CharField(max_length=100, null=True)),
                ('flightnumber', models.CharField(default='Inconnu', max_length=100)),
                ('departureairportcode', models.CharField(max_length=100, null=True)),
                ('landingairportcode', models.CharField(max_length=100, null=True)),
                ('departuretime', models.DateTimeField(null=True)),
                ('landingtime', models.DateTimeField(null=True)),
                ('pnr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AmadeusDecoder.pnr')),
            ],
            options={
                'db_table': 't_pnr_flight',
            },
            bases=(models.Model, AmadeusDecoder.models.BaseModel.BaseModel),
        ),
        migrations.CreateModel(
            name='Fee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=200, null=True)),
                ('designation', models.CharField(max_length=200, null=True)),
                ('value', models.DecimalField(decimal_places=4, default=0.0, max_digits=11)),
                ('cost', models.DecimalField(decimal_places=4, default=0.0, max_digits=11)),
                ('tax', models.DecimalField(decimal_places=4, default=0.0, max_digits=11)),
                ('total', models.DecimalField(decimal_places=4, default=0.0, max_digits=11)),
                ('pnr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AmadeusDecoder.pnr')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AmadeusDecoder.ticket')),
            ],
            options={
                'db_table': 't_fee',
            },
            bases=(models.Model, AmadeusDecoder.models.BaseModel.BaseModel),
        ),
        migrations.CreateModel(
            name='CurrencyRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=4, default=0.0, max_digits=10)),
                ('lastupdate', models.DateTimeField(default=django.utils.timezone.now)),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AmadeusDecoder.currency')),
            ],
            options={
                'db_table': 't_currency_rate',
            },
            bases=(models.Model, AmadeusDecoder.models.BaseModel.BaseModel),
        ),
        migrations.AddConstraint(
            model_name='currency',
            constraint=models.UniqueConstraint(fields=('code',), name='unique_currency_code'),
        ),
        migrations.AddConstraint(
            model_name='currency',
            constraint=models.UniqueConstraint(fields=('name',), name='unique_currency_name'),
        ),
        migrations.AddField(
            model_name='contact',
            name='pnr',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AmadeusDecoder.pnr'),
        ),
        migrations.AddField(
            model_name='config',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AmadeusDecoder.user'),
        ),
        migrations.AddField(
            model_name='clientaddress',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AmadeusDecoder.client'),
        ),
        migrations.AddConstraint(
            model_name='airport',
            constraint=models.UniqueConstraint(fields=('iata_code',), name='unique_airport_iata_code'),
        ),
        migrations.AddField(
            model_name='activation',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AmadeusDecoder.user'),
        ),
        migrations.AddConstraint(
            model_name='pnr',
            constraint=models.UniqueConstraint(fields=('number',), name='unique_pnr'),
        ),
    ]
