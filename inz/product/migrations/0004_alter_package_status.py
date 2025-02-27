# Generated by Django 4.2 on 2023-07-24 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_package_received_at_alter_package_sent_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='status',
            field=models.CharField(choices=[('AWAITING_PICKUP', 'Przyjęta do recepcji'), ('RECEIVED', 'Paczka odebrana przez klienta'), ('READY', 'Gotowa do odbioru'), ('SENT', 'Odebrana przez kuriera')], default='AWAITING_PICKUP', max_length=15, verbose_name='Status'),
        ),
    ]
