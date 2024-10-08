# Generated by Django 4.0.6 on 2022-11-14 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AmadeusDecoder', '0130_pnr_is_invoiced'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='is_prime',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='ticket',
            name='issuing_agency',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='emitted_tickets', to='AmadeusDecoder.office'),
        ),
    ]
