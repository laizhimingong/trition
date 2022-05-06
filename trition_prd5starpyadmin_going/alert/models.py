from django.db import models

# Create your models here.
#历史告警表
class HistoryAlert(models.Model):
    alertname = models.CharField(max_length=100, verbose_name='告警名称')
    status = models.CharField(max_length=20, verbose_name='状态', blank=True)
    severity = models.CharField(max_length=20, verbose_name='告警级别', blank=True)
    env = models.CharField(max_length=20, verbose_name='环境', blank=True)
    idc = models.CharField(max_length=20, verbose_name='机房', blank=True)
    business = models.CharField(max_length=20, verbose_name='业务', blank=True)
    instance = models.CharField(max_length=50, verbose_name='实例', blank=True)
    ip = models.CharField(max_length=50, verbose_name='IP', blank=True)
    port = models.CharField(max_length=50, verbose_name='PORT', blank=True)
    summary = models.CharField(max_length=1000, verbose_name='告警主旨', blank=True)
    description = models.CharField(max_length=1000, verbose_name='告警信息', blank=True)
    startsAt = models.CharField(max_length=80,verbose_name='告警产生时间',blank=True)
    endsAt = models.CharField(max_length=80,verbose_name='告警恢复时间',blank=True)
    sendtime = models.CharField(max_length=80,verbose_name='告警发送时间',blank=True)
    caltime = models.CharField(max_length=80, verbose_name='异常时间', blank=True)
    fingerprint = models.CharField(max_length=80, verbose_name='fingerprint', blank=True)
    def __str__(self):
        return self.alertname
    class Meta:
        db_table = 'history_alert'
        ordering = ['-sendtime']  # 按告警发送时间倒排

#实时告警表
class TimeAlert(models.Model):
    alertname = models.CharField(max_length=100, verbose_name='告警名称')
    status = models.CharField(max_length=20, verbose_name='状态', blank=True)
    severity = models.CharField(max_length=20, verbose_name='告警级别', blank=True)
    env = models.CharField(max_length=20, verbose_name='环境', blank=True)
    idc = models.CharField(max_length=20, verbose_name='机房', blank=True)
    business = models.CharField(max_length=20, verbose_name='业务', blank=True)
    instance = models.CharField(max_length=50, verbose_name='实例', blank=True)
    ip = models.CharField(max_length=50, verbose_name='IP', blank=True)
    port = models.CharField(max_length=50, verbose_name='PORT', blank=True)
    summary = models.CharField(max_length=1000, verbose_name='告警主旨', blank=True)
    description = models.CharField(max_length=1000, verbose_name='告警信息', blank=True)
    startsAt = models.CharField(max_length=80,verbose_name='告警产生时间',blank=True)
    endsAt = models.CharField(max_length=80,verbose_name='告警恢复时间',blank=True)
    sendtime = models.CharField(max_length=80,verbose_name='告警发送时间',blank=True)
    caltime = models.CharField(max_length=80, verbose_name='异常时间', blank=True)
    fingerprint = models.CharField(max_length=80, verbose_name='fingerprint', blank=True)
    def __str__(self):
        return self.alertname
    class Meta:
        db_table = 'time_alert'
        ordering = ['-sendtime']  # 按告警发送时间倒排

# consul注册服务表
class ServicesRegister(models.Model):
    id = models.IntegerField(primary_key=True)
    service_id = models.CharField(max_length=100, verbose_name='服务ID')
    ip = models.CharField(max_length=20, verbose_name='地址')
    port = models.CharField(max_length=10, verbose_name='端口')
    business = models.CharField(max_length=40, verbose_name='业务')
    idc = models.CharField(max_length=20, verbose_name='归属机房')
    env = models.CharField(max_length=20, verbose_name='服务环境')
    hostname = models.CharField(max_length=100, verbose_name='主机名')
    exporter = models.CharField(max_length=40, verbose_name='exporter')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    def __str__(self):
        return self.ip
    class Meta:
        db_table = 'services'
        ordering = ['id']   # 按排序 升序