# Generated by Django 3.2.4 on 2021-07-07 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alert', '0011_timealert'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServicesRegister',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('service_id', models.CharField(max_length=100, verbose_name='服务ID')),
                ('ip', models.CharField(max_length=20, verbose_name='地址')),
                ('port', models.CharField(max_length=10, verbose_name='端口')),
                ('business', models.CharField(max_length=40, verbose_name='业务')),
                ('idc', models.CharField(max_length=20, verbose_name='归属机房')),
                ('env', models.CharField(max_length=20, verbose_name='服务环境')),
                ('hostname', models.CharField(max_length=100, verbose_name='主机名')),
                ('exporter', models.CharField(max_length=40, verbose_name='exporter')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'db_table': 'services',
                'ordering': ['id'],
            },
        ),
    ]
