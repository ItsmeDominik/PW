# Generated by Django 4.2 on 2023-08-18 21:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0018_offers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='offers',
            old_name='klient',
            new_name='client',
        ),
    ]
