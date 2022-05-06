# Generated by Django 3.2.4 on 2021-10-08 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0027_auto_20210913_1442'),
    ]

    operations = [
        migrations.CreateModel(
            name='elkNginxStatus404',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('status_404', models.CharField(blank=True, max_length=5, null=True, verbose_name='status404')),
            ],
            options={
                'db_table': 'elkNginxStatus404',
                'ordering': ['id'],
            },
        ),
    ]
