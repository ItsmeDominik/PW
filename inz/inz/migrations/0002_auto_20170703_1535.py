# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-03 15:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inz', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='done',
            field=models.BooleanField(default=False),
        ),
    ]
