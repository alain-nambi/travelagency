# Generated by Django 4.0.6 on 2022-09-02 08:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AmadeusDecoder', '0020_alter_contact_pnr'),
    ]

    operations = [
        migrations.AddField(
            model_name='office',
            name='code',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddConstraint(
            model_name='office',
            constraint=models.UniqueConstraint(fields=('code',), name='unique_office'),
        ),
        migrations.AddField(
            model_name='pnr',
            name='agency',
            field=models.ForeignKey(db_column='agency_code', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pnrs', to='AmadeusDecoder.office', to_field='code'),
        ),
        migrations.AlterField(
            model_name='pnr',
            name='currency',
            field=models.ForeignKey(db_column='currency_code', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pnrs', to='AmadeusDecoder.currency', to_field='code'),
        ),
    ]
