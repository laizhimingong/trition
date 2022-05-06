# Generated by Django 3.2.4 on 2021-08-16 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0021_alter_product_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nomonitorcmdb',
            name='cmdb_id',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='服务ID'),
        ),
        migrations.AlterField(
            model_name='nomonitorcmdb',
            name='cpuinfo',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='CPU'),
        ),
        migrations.AlterField(
            model_name='nomonitorcmdb',
            name='createtime',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='nomonitorcmdb',
            name='datacenter',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='归属机房'),
        ),
        migrations.AlterField(
            model_name='nomonitorcmdb',
            name='diskinfo',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='磁盘'),
        ),
        migrations.AlterField(
            model_name='nomonitorcmdb',
            name='hostname',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='主机名'),
        ),
        migrations.AlterField(
            model_name='nomonitorcmdb',
            name='meminfo',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='内存'),
        ),
        migrations.AlterField(
            model_name='nomonitorcmdb',
            name='modifytime',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='修改时间'),
        ),
        migrations.AlterField(
            model_name='nomonitorcmdb',
            name='projectadmin',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='产品管理员'),
        ),
        migrations.AlterField(
            model_name='nomonitorcmdb',
            name='projectenv',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='服务环境'),
        ),
        migrations.AlterField(
            model_name='nomonitorcmdb',
            name='projectname',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='产品'),
        ),
        migrations.AlterField(
            model_name='nomonitorcmdb',
            name='serverip',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='地址'),
        ),
        migrations.AlterField(
            model_name='nomonitorcmdb',
            name='status',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='虚机状态'),
        ),
        migrations.AlterField(
            model_name='nomonitorcmdb',
            name='update_time',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间'),
        ),
    ]
