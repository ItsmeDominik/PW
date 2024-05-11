# Generated by Django 4.2 on 2023-08-12 07:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_alter_company_options'),
        ('reservation', '0006_room_destination_room_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomreservation',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='company.company'),
        ),
    ]
