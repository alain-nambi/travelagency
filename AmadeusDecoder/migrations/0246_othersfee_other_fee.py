# Generated by Django 4.1.7 on 2023-05-26 08:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AmadeusDecoder', '0245_alter_othersfee_creation_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='othersfee',
            name='other_fee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='others_fees', to='AmadeusDecoder.othersfee'),
        ),
    ]
