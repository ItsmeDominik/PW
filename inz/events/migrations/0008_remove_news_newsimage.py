# Generated by Django 4.2 on 2023-07-10 19:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_alter_news_newsimage_alter_news_newsname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='newsImage',
        ),
    ]
