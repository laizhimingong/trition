# Generated by Django 3.2.4 on 2021-09-13 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0026_auto_20210827_1009'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='nomonitorcmdb',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='todaycmdb',
            options={'ordering': ['id']},
        ),
    ]