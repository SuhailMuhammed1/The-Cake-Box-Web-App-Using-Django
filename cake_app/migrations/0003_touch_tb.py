# Generated by Django 3.1.5 on 2021-04-16 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cake_app', '0002_bill_tb'),
    ]

    operations = [
        migrations.CreateModel(
            name='touch_tb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('email', models.CharField(default='', max_length=100)),
            ],
        ),
    ]
