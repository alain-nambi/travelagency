# Generated by Django 4.0.6 on 2022-08-30 06:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AmadeusDecoder', '0007_pnr_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pnr',
            name='currency',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='currency_code', to='AmadeusDecoder.currency', to_field='code'),
        ),
    ]
