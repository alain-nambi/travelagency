# Generated by Django 4.0.6 on 2022-09-12 08:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AmadeusDecoder', '0044_alter_ticket_passenger'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='passenger',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ticket', to='AmadeusDecoder.passenger'),
        ),
    ]
