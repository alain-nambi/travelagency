# Generated by Django 4.0.6 on 2022-09-02 11:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AmadeusDecoder', '0026_alter_passengerattribute_passenger_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='passengerattribute',
            name='type',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='pnrpassenger',
            name='passenger',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='AmadeusDecoder.passenger'),
        ),
    ]
