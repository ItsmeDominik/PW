# Generated by Django 4.2 on 2023-08-23 22:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_alter_order_options_alter_product_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Zamówienia', 'verbose_name_plural': 'Zamówienia'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Produkty', 'verbose_name_plural': 'Produkty'},
        ),
    ]
