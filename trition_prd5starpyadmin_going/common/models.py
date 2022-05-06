from django.db import models


# Create your models here.
# 产品表
class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    projectname = models.CharField(max_length=40, verbose_name='所属产品', blank=True)
    createtime = models.CharField(max_length=50, verbose_name='创建时间', blank=True)
    modifytime = models.CharField(max_length=50, verbose_name='修改时间', blank=True)
    status = models.CharField(max_length=50, verbose_name='状态', blank=True, null=True)

    def __str__(self):
        return self.projectname

    class Meta:
        db_table = 'Product'
        # ordering = ['status']  # 按排序


# cmdb服务表
class Cmdb(models.Model):
    id = models.IntegerField(primary_key=True)
    cmdb_id = models.CharField(max_length=100, verbose_name='服务ID', blank=True, null=True)
    hostname = models.CharField(max_length=100, verbose_name='主机名', blank=True, null=True)
    serverip = models.CharField(max_length=20, verbose_name='地址', blank=True, null=True)
    cpuinfo = models.CharField(max_length=20, verbose_name='CPU', blank=True, null=True)
    diskinfo = models.CharField(max_length=20, verbose_name='磁盘', blank=True, null=True)
    meminfo = models.CharField(max_length=20, verbose_name='内存', blank=True, null=True)
    projectname = models.CharField(max_length=40, verbose_name='产品', blank=True, null=True)
    ostype = models.CharField(max_length=40, null=True, verbose_name='机器类型', blank=True)
    datacenter = models.CharField(max_length=20, verbose_name='归属机房', blank=True, null=True)
    projectenv = models.CharField(max_length=20, verbose_name='服务环境', blank=True, null=True)
    projectadmin = models.CharField(max_length=20, verbose_name='产品管理员', blank=True, null=True)
    createtime = models.CharField(max_length=50, verbose_name='创建时间', blank=True, null=True)
    modifytime = models.CharField(max_length=50, verbose_name='修改时间', blank=True, null=True)
    status = models.CharField(max_length=50, verbose_name='虚机状态', blank=True, null=True)
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间', blank=True, null=True)

    def __str__(self):
        return self.serverip

    class Meta:
        db_table = 'cmdb_info'
        ordering = ['-createtime']  # 按排序


class NoMonitorCmdb(models.Model):
    id = models.IntegerField(primary_key=True)
    cmdb_id = models.CharField(max_length=100, verbose_name='服务ID', blank=True, null=True)
    hostname = models.CharField(max_length=100, verbose_name='主机名', blank=True, null=True)
    serverip = models.CharField(max_length=20, verbose_name='地址', blank=True, null=True)
    cpuinfo = models.CharField(max_length=20, verbose_name='CPU', blank=True, null=True)
    diskinfo = models.CharField(max_length=20, verbose_name='磁盘', blank=True, null=True)
    meminfo = models.CharField(max_length=20, verbose_name='内存', blank=True, null=True)
    projectname = models.CharField(max_length=40, verbose_name='产品', blank=True, null=True)
    ostype = models.CharField(max_length=40, null=True, verbose_name='机器类型', blank=True)
    datacenter = models.CharField(max_length=20, verbose_name='归属机房', blank=True, null=True)
    projectenv = models.CharField(max_length=20, verbose_name='服务环境', blank=True, null=True)
    projectadmin = models.CharField(max_length=20, verbose_name='产品管理员', blank=True, null=True)
    createtime = models.CharField(max_length=50, verbose_name='创建时间', blank=True, null=True)
    modifytime = models.CharField(max_length=50, verbose_name='修改时间', blank=True, null=True)
    status = models.CharField(max_length=50, verbose_name='虚机状态', blank=True, null=True)
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间', blank=True, null=True)

    def __str__(self):
        return self.serverip

    class Meta:
        db_table = 'NoMonitorCmdb'
        ordering = ['-createtime']  # 按排序


class TodayCmdb(models.Model):
    id = models.IntegerField(primary_key=True)
    cmdb_id = models.CharField(max_length=100, verbose_name='服务ID', blank=True, null=True)
    hostname = models.CharField(max_length=100, verbose_name='主机名', blank=True, null=True)
    serverip = models.CharField(max_length=20, verbose_name='地址', blank=True, null=True)
    cpuinfo = models.CharField(max_length=20, verbose_name='CPU', blank=True, null=True)
    diskinfo = models.CharField(max_length=20, verbose_name='磁盘', blank=True, null=True)
    meminfo = models.CharField(max_length=20, verbose_name='内存', blank=True, null=True)
    projectname = models.CharField(max_length=40, verbose_name='产品', blank=True, null=True)
    ostype = models.CharField(max_length=40, null=True, verbose_name='机器类型', blank=True)
    datacenter = models.CharField(max_length=20, verbose_name='归属机房', blank=True, null=True)
    projectenv = models.CharField(max_length=20, verbose_name='服务环境', blank=True, null=True)
    projectadmin = models.CharField(max_length=20, verbose_name='产品管理员', blank=True, null=True)
    createtime = models.CharField(max_length=50, verbose_name='创建时间', blank=True, null=True)
    modifytime = models.CharField(max_length=50, verbose_name='修改时间', blank=True, null=True)
    status = models.CharField(max_length=50, verbose_name='虚机状态', blank=True, null=True)
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间', blank=True, null=True)

    def __str__(self):
        return self.serverip

    class Meta:
        db_table = 'TodayCmdb'
        ordering = ['id']  # 按排序


# 数据库关系表
class MysqlReplication(models.Model):
    id = models.IntegerField(primary_key=True)
    projectname = models.CharField(max_length=40, verbose_name='business', blank=True, null=True)
    rp = models.CharField(max_length=10, verbose_name='rp', blank=True, null=True)
    master_ip = models.CharField(max_length=40, verbose_name='master_ip', blank=True, null=True)
    slave_ip = models.CharField(max_length=40, verbose_name='slave_ip', blank=True, null=True)
    rp_status = models.CharField(max_length=40, verbose_name='rp_status', blank=True, null=True)

    class Meta:
        db_table = 'mysql_replication'
        ordering = ['id']  # 按排序


class CancellationRecord(models.Model):
    service_id = models.CharField(max_length=80, verbose_name='服务注册ID', blank=True, null=True)
    record_time = models.CharField(max_length=80, verbose_name='注销时间', blank=True, null=True)

    class Meta:
        db_table = 'CancellationRecord'
        ordering = ['record_time']  # 按排序

class elkNginxStatus404(models.Model):
    status_404 = models.CharField(max_length=5, verbose_name='status404', blank=True, null=True)
    search_time= models.CharField(max_length=40, verbose_name='search_time', blank=True, null=True)
    search_time_stamp= models.CharField(max_length=40, verbose_name='search_time', blank=True, null=True)

    class Meta:
        db_table = 'elkNginxStatus404'
        ordering = ['id']  # 按排序

class elkNginxStatus500(models.Model):
    status_500 = models.CharField(max_length=5, verbose_name='status500', blank=True, null=True)
    search_time= models.CharField(max_length=40, verbose_name='search_time', blank=True, null=True)
    search_time_stamp= models.CharField(max_length=40, verbose_name='search_time', blank=True, null=True)

    class Meta:
        db_table = 'elkNginxStatus500'
        ordering = ['id']  # 按排序