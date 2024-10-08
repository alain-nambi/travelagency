# Generated by Django 4.0.6 on 2022-08-31 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AmadeusDecoder', '0015_alter_user_office'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pnr',
            name='agent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pnrs', to='AmadeusDecoder.user'),
        ),
        migrations.AlterField(
            model_name='pnr',
            name='currency',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pnrs', to='AmadeusDecoder.currency', to_field='code'),
        ),
    ]
