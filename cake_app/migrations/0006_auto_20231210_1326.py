# Generated by Django 3.1.5 on 2023-12-10 07:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cake_app', '0005_auto_20231210_1325'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product_tb',
            old_name='created_at',
            new_name='createdat',
        ),
    ]