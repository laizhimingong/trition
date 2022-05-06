# Generated by Django 3.2.4 on 2021-07-08 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cmdb',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('cmdb_id', models.CharField(max_length=100, verbose_name='服务ID')),
                ('hostname', models.CharField(max_length=100, verbose_name='主机名')),
                ('serverip', models.CharField(max_length=20, verbose_name='地址')),
                ('cpuinfo', models.CharField(max_length=20, verbose_name='CPU')),
                ('diskinfo', models.CharField(max_length=20, verbose_name='磁盘')),
                ('meminfo', models.CharField(max_length=20, verbose_name='内存')),
                ('projectname', models.CharField(max_length=40, verbose_name='业务')),
                ('ostype', models.CharField(max_length=40, null=True, verbose_name='机器类型')),
                ('datacenter', models.CharField(max_length=20, verbose_name='归属机房')),
                ('projectenv', models.CharField(max_length=20, verbose_name='服务环境')),
                ('projectadmin', models.CharField(max_length=20, verbose_name='产品管理员')),
                ('createtime', models.CharField(max_length=50, verbose_name='创建时间')),
                ('modifytime', models.CharField(max_length=50, verbose_name='修改时间')),
                ('status', models.CharField(max_length=50, verbose_name='虚机状态')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'db_table': 'cmdb_info',
                'ordering': ['-createtime'],
            },
        ),
        migrations.DeleteModel(
            name='test',
        ),
    ]
