# Generated by Django 4.2 on 2023-08-23 22:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0024_alter_discount_options_alter_news_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='discount',
            options={'verbose_name': 'Rabat', 'verbose_name_plural': 'Rabat'},
        ),
        migrations.AlterModelOptions(
            name='news',
            options={'verbose_name': 'Wydarzenia', 'verbose_name_plural': 'Wydarzenia'},
        ),
    ]
