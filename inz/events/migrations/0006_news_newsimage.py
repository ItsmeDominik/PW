# Generated by Django 4.2 on 2023-07-10 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_alter_events_options_alter_news_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='newsImage',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
