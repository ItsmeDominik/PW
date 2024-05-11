# Generated by Django 4.2 on 2023-06-20 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('companyName', models.CharField(max_length=256)),
                ('zipCode', models.CharField(max_length=10)),
                ('nip', models.CharField(max_length=20)),
                ('businessArea', models.CharField(choices=[('design', 'Design'), ('it', 'IT'), ('co-working', 'Co-working'), ('real estate', 'Real estate'), ('customer service', 'Customer service'), ('data analysis', 'Data analysis'), ('programing', 'Programing'), ('marketing', 'Marketing'), ('financed', 'Financed'), ('insurance', 'Insurance'), ('architecture', 'Architecture')], default='customer service', max_length=32)),
            ],
        ),
    ]
