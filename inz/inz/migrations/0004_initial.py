# Generated by Django 4.2 on 2023-06-20 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inz', '0003_delete_todo'),
    ]

    operations = [
        migrations.CreateModel(
            name='company',
            fields=[
                ('companyID', models.AutoField(primary_key=True, serialize=False)),
                ('companyName', models.CharField(max_length=100)),
                ('companyNIP', models.IntegerField()),
                ('companyRoad', models.CharField(max_length=200)),
                ('companyCity', models.CharField(max_length=100)),
                ('companyZipCode', models.IntegerField()),
            ],
        ),
    ]
