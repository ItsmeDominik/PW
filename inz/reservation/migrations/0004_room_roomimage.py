# Generated by Django 4.2 on 2023-07-26 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0003_alter_room_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='roomImage',
            field=models.ImageField(blank=True, null=True, upload_to='images', verbose_name='Image'),
        ),
    ]
