# Generated by Django 4.2 on 2023-08-05 08:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0009_alter_comment_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='creation_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Godzina utowrzenia'),
            preserve_default=False,
        ),
    ]
