# Generated by Django 3.2.4 on 2021-10-11 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0029_elknginxstatus404_search_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='elkNginxStatus500',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('status_404', models.CharField(blank=True, max_length=5, null=True, verbose_name='status500')),
                ('search_time', models.CharField(blank=True, max_length=40, null=True, verbose_name='search_time')),
            ],
            options={
                'db_table': 'elkNginxStatus500',
                'ordering': ['id'],
            },
        ),
    ]
