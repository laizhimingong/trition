# Generated by Django 3.2.4 on 2021-10-11 09:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0030_elknginxstatus500'),
    ]

    operations = [
        migrations.RenameField(
            model_name='elknginxstatus500',
            old_name='status_404',
            new_name='status_500',
        ),
    ]