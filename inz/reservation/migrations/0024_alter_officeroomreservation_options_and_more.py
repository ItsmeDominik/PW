# Generated by Django 4.2 on 2023-08-23 22:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0023_alter_officeroomreservation_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='officeroomreservation',
            options={'verbose_name': 'OfficeRoomReservation', 'verbose_name_plural': 'OfficeRoomReservation'},
        ),
        migrations.AlterModelOptions(
            name='printerrent',
            options={'verbose_name': 'PrinterRent', 'verbose_name_plural': 'PrinterRent'},
        ),
        migrations.AlterModelOptions(
            name='printers',
            options={'verbose_name': 'Printers', 'verbose_name_plural': 'Printers'},
        ),
        migrations.AlterModelOptions(
            name='room',
            options={'verbose_name': 'Room', 'verbose_name_plural': 'Room'},
        ),
        migrations.AlterModelOptions(
            name='roomreservation',
            options={'verbose_name': 'RoomReservation', 'verbose_name_plural': 'RoomReservation'},
        ),
    ]
