# Generated by Django 4.2 on 2023-07-22 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_remove_package_company_package_package_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='received_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Data przyjęcia'),
        ),
        migrations.AlterField(
            model_name='package',
            name='sent_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Data nadania'),
        ),
    ]
