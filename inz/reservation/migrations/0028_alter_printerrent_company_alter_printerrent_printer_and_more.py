# Generated by Django 4.2 on 2023-08-27 10:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0011_alter_company_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reservation', '0027_alter_officeroomreservation_company_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='printerrent',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.company', verbose_name='Firma'),
        ),
        migrations.AlterField(
            model_name='printerrent',
            name='printer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservation.printers', verbose_name='Drukarka'),
        ),
        migrations.AlterField(
            model_name='printerrent',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Użytkownik'),
        ),
        migrations.AlterField(
            model_name='roomreservation',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.company', verbose_name='Firma'),
        ),
        migrations.AlterField(
            model_name='roomreservation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Użytkownik'),
        ),
    ]
