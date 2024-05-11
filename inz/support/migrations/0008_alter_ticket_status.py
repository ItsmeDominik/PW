# Generated by Django 4.2 on 2023-07-24 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0007_alter_ticket_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(choices=[('new', 'New'), ('inProgress', 'In Progess'), ('resolved', 'Resolved')], default='new', max_length=200, verbose_name='Status'),
        ),
    ]
