# Generated by Django 4.2 on 2023-08-16 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0015_alter_printers_date_of_last_service_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='printers',
            name='status',
            field=models.CharField(choices=[('in_use', 'W Użyciu'), ('service', 'Na Serwisie')], default='in_use', max_length=32, verbose_name='Status'),
        ),
    ]
