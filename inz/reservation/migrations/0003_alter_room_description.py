# Generated by Django 4.2 on 2023-07-22 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0002_rename_rommreservation_roomreservation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='description',
            field=models.TextField(verbose_name='Opis'),
        ),
    ]
