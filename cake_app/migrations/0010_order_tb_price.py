# Generated by Django 3.1.5 on 2023-12-16 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cake_app', '0009_remove_product_tb_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_tb',
            name='price',
            field=models.CharField(default='', max_length=100),
        ),
    ]
