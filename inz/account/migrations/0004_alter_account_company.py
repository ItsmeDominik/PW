# Generated by Django 4.2 on 2023-06-20 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_account_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='company',
            field=models.CharField(max_length=256),
        ),
    ]
