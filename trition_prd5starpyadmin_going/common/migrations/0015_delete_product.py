# Generated by Django 3.2.4 on 2021-08-13 17:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0014_remove_product_status'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Product',
        ),
    ]
