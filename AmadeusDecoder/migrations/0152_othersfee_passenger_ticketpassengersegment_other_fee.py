# Generated by Django 4.0.6 on 2022-11-28 10:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AmadeusDecoder', '0151_remove_ticketpassengersegment_other_fee'),
    ]

    operations = [
        migrations.AddField(
            model_name='othersfee',
            name='passenger',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='others_fees', to='AmadeusDecoder.passenger'),
        ),
        migrations.AddField(
            model_name='ticketpassengersegment',
            name='other_fee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_segments', to='AmadeusDecoder.othersfee'),
        ),
    ]
