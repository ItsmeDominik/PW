# Generated by Django 4.2 on 2023-08-27 10:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '0011_alter_company_options'),
        ('reservation', '0026_alter_officeroomreservation_room_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='officeroomreservation',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.company', verbose_name='Firma'),
        ),
        migrations.AlterField(
            model_name='officeroomreservation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Użytkownik'),
        ),
    ]
